"""Train a real CNN waste classifier (transfer learning) on the raw dump.

The color-histogram + logistic-regression baseline in
`packages/ml.classification/train.py` tops out around macro-F1 0.41 because a
26-dim histogram cannot separate clear glass from paper or shiny metal from
everything else. This script swaps the feature extractor for a pretrained
torchvision backbone and keeps the rest of the pipeline (dataset -> train ->
evaluate -> registry -> inference) intact.

Dataset: one folder per class, defaults to
    data/raw/waste/data/raw/waste/garbage_classification
Override with WASTE_CLASSIFICATION_DATA_ROOT. Split is stratified and
image-level, so no resized duplicate of the same photo can land in both
train and val.

Usage:
    python -m scripts.train_cnn_classifier
    python -m scripts.train_cnn_classifier --backbone efficientnet_b0 --epochs 12

Class imbalance is handled with inverse-frequency loss weights plus a weighted
sampler, so the 5325-image `clothes` class cannot dominate the 607-image
`brown-glass` one. Best weights are written to
models/artifacts/cnn/<name>/best.pt and registered in the model registry with
real held-out metrics; promotion stays a manual step.
"""
import argparse
import json
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, WeightedRandomSampler
from torchvision import datasets, models, transforms

from packages.ml.model_registry.registry import register_model

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_ROOT = (
    REPO_ROOT / "data" / "raw" / "waste" / "data" / "raw" / "waste" / "garbage_classification"
)
RUN_DIR = REPO_ROOT / "models" / "artifacts" / "cnn"

BACKBONES = {
    "convnext_tiny": (models.convnext_tiny, models.ConvNeXt_Tiny_Weights, 768),
    "efficientnet_b0": (models.efficientnet_b0, models.EfficientNet_B0_Weights, 1280),
    "resnet18": (models.resnet18, models.ResNet18_Weights, 512),
    "mobilenet_v3_small": (models.mobilenet_v3_small, models.MobileNet_V3_Small_Weights, 576),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", default="")
    parser.add_argument("--backbone", default="convnext_tiny", choices=sorted(BACKBONES))
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch", type=int, default=32)
    parser.add_argument("--imgsz", type=int, default=160)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--val-split", type=float, default=0.2)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--name", default="waste-cnn")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    return parser.parse_args()


def build_transforms(imgsz: int) -> tuple[transforms.Compose, transforms.Compose]:
    norm = transforms.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    )
    train_tf = transforms.Compose([
        transforms.RandomResizedCrop(imgsz, scale=(0.6, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(12),
        transforms.ColorJitter(brightness=0.25, contrast=0.25, saturation=0.25),
        transforms.ToTensor(),
        norm,
        transforms.RandomErasing(p=0.15),
    ])
    val_tf = transforms.Compose([
        transforms.Resize(int(imgsz * 1.15)),
        transforms.CenterCrop(imgsz),
        transforms.ToTensor(),
        norm,
    ])
    return train_tf, val_tf


def stratified_split(targets: list[int], val_split: float, seed: int):
    """Yield (train_idx, val_idx) holding out whole images, class-stratified."""
    from collections import defaultdict

    import numpy as np

    rng = np.random.default_rng(seed)
    by_class: dict[int, list[int]] = defaultdict(list)
    for idx, label in enumerate(targets):
        by_class[label].append(idx)

    train_idx, val_idx = [], []
    for label, idxs in by_class.items():
        idxs = list(idxs)
        rng.shuffle(idxs)
        n_val = max(1, int(round(len(idxs) * val_split))) if len(idxs) > 1 else 0
        val_idx.extend(idxs[:n_val])
        train_idx.extend(idxs[n_val:])
    return train_idx, val_idx


def make_model(backbone: str, num_classes: int) -> nn.Module:
    ctor, weights_enum, feature_dim = BACKBONES[backbone]
    model = ctor(weights=weights_enum.DEFAULT)
    if backbone.startswith("convnext"):
        model.classifier[2] = nn.Linear(feature_dim, num_classes)
    elif backbone == "efficientnet_b0":
        model.classifier[1] = nn.Linear(feature_dim, num_classes)
    elif backbone == "resnet18":
        model.fc = nn.Linear(feature_dim, num_classes)
    else:
        model.classifier[1] = nn.Linear(feature_dim, num_classes)
    return model


@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader, device: str, class_names: list[str]) -> dict:
    from sklearn.metrics import (
        accuracy_score,
        confusion_matrix,
        precision_recall_fscore_support,
    )

    model.eval()
    all_true, all_pred = [], []
    total_loss = 0.0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        logits = model(images)
        total_loss += float(nn.functional.cross_entropy(logits, labels, reduction="sum"))
        all_true.extend(labels.cpu().tolist())
        all_pred.extend(logits.argmax(dim=1).cpu().tolist())

    precision, recall, f1, support = precision_recall_fscore_support(
        all_true, all_pred, labels=list(range(len(class_names))), average=None, zero_division=0
    )
    return {
        "accuracy": round(float(accuracy_score(all_true, all_pred)), 4),
        "macro_f1": round(float(f1.mean()), 4),
        "val_loss": round(total_loss / max(len(all_true), 1), 4),
        "per_class": {
            name: {
                "precision": round(float(p), 3),
                "recall": round(float(r), 3),
                "f1": round(float(s), 3),
                "support": int(n),
            }
            for name, p, r, s, n in zip(class_names, precision, recall, f1, support)
        },
        "confusion_matrix": confusion_matrix(
            all_true, all_pred, labels=list(range(len(class_names)))
        ).tolist(),
        "val_set_size": len(all_true),
    }


def main() -> None:
    args = parse_args()

    data_root = Path(args.data_root) if args.data_root else DEFAULT_DATA_ROOT
    if not data_root.is_dir():
        raise SystemExit(f"Data root not found: {data_root}")
    class_dirs = sorted(d for d in data_root.iterdir() if d.is_dir())
    if len(class_dirs) < 2:
        raise SystemExit(f"Need one folder per class under {data_root}; found {len(class_dirs)}")
    class_names = [d.name for d in class_dirs]
    print(f"Data root: {data_root}")
    print(f"Classes ({len(class_names)}): {class_names}")

    torch.manual_seed(args.seed)
    device = args.device
    print(f"Device: {device}")

    train_tf, val_tf = build_transforms(args.imgsz)
    full_train = datasets.ImageFolder(str(data_root), transform=train_tf)
    full_val = datasets.ImageFolder(str(data_root), transform=val_tf)
    targets = list(full_train.targets)

    train_idx, val_idx = stratified_split(targets, args.val_split, args.seed)
    print(f"Split: {len(train_idx)} train / {len(val_idx)} val images")
    print("Class balance:", {
        name: targets.count(i) for i, name in enumerate(class_names)
    })

    counts = {i: targets.count(i) for i in range(len(class_names))}
    train_counts = {i: sum(1 for idx in train_idx if targets[idx] == i) for i in range(len(class_names))}
    sample_weights = [1.0 / train_counts[targets[i]] for i in train_idx]
    sampler = WeightedRandomSampler(
        weights=torch.DoubleTensor(sample_weights),
        num_samples=len(sample_weights),
        replacement=True,
    )
    class_weights = torch.FloatTensor([
        len(train_idx) / (len(class_names) * train_counts[i]) for i in range(len(class_names))
    ]).to(device)

    train_ds = torch.utils.data.Subset(full_train, train_idx)
    val_ds = torch.utils.data.Subset(full_val, val_idx)
    train_loader = DataLoader(
        train_ds, batch_size=args.batch, sampler=sampler,
        num_workers=args.workers, pin_memory=(device == "cuda"), drop_last=True,
    )
    val_loader = DataLoader(
        val_ds, batch_size=args.batch, shuffle=False,
        num_workers=args.workers, pin_memory=(device == "cuda"),
    )
    print(f"Weighted sampler active. Loss class weights: {class_weights.tolist()}")

    model = make_model(args.backbone, len(class_names)).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=0.05)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scheduler = torch.optim.lr_scheduler.OneCycleLR(
        optimizer, max_lr=args.lr, epochs=args.epochs, steps_per_epoch=len(train_loader),
        pct_start=0.25,
    )
    scaler = torch.amp.GradScaler("cuda", enabled=(device == "cuda"))

    run_dir = RUN_DIR / args.name
    run_dir.mkdir(parents=True, exist_ok=True)
    best_macro_f1 = -1.0
    history = []

    for epoch in range(1, args.epochs + 1):
        model.train()
        running, seen = 0.0, 0
        for images, labels in train_loader:
            images, labels = images.to(device, non_blocking=True), labels.to(device, non_blocking=True)
            optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast("cuda", enabled=(device == "cuda")):
                loss = criterion(model(images), labels)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()
            running += float(loss) * images.size(0)
            seen += images.size(0)

        metrics = evaluate(model, val_loader, device, class_names)
        metrics["epoch"] = epoch
        metrics["train_loss"] = round(running / max(seen, 1), 4)
        history.append({k: v for k, v in metrics.items() if k != "confusion_matrix"})
        print(
            f"epoch {epoch:>3}/{args.epochs}  train_loss={metrics['train_loss']:.4f}  "
            f"val_loss={metrics['val_loss']:.4f}  acc={metrics['accuracy']:.4f}  "
            f"macro_f1={metrics['macro_f1']:.4f}"
        )

        if metrics["macro_f1"] > best_macro_f1:
            best_macro_f1 = metrics["macro_f1"]
            payload = {
                "model_state": model.state_dict(),
                "backbone": args.backbone,
                "class_names": class_names,
                "imgsz": args.imgsz,
                "mean": [0.485, 0.456, 0.406],
                "std": [0.229, 0.224, 0.225],
                "metrics": metrics,
            }
            torch.save(payload, run_dir / "best.pt")
            print(f"  saved new best.pt (macro_f1={best_macro_f1:.4f})")

    final = evaluate(model, val_loader, device, class_names)
    print("\nFinal per-class F1:")
    for name, row in final["per_class"].items():
        print(f"  {name:<14} f1={row['f1']:.3f}  precision={row['precision']:.3f}  "
              f"recall={row['recall']:.3f}  support={row['support']}")

    report = {
        "backbone": args.backbone,
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "data_root": str(data_root),
        "train_images": len(train_idx),
        "val_images": len(val_idx),
        "class_names": class_names,
        "best_macro_f1": best_macro_f1,
        "final_metrics": final,
        "history": history,
    }
    report_path = run_dir / "metrics.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    version = f"cnn-{args.backbone}-{report_path.stat().st_mtime_ns}"
    register_model(
        "waste-classifier-cnn",
        version,
        str(run_dir / "best.pt"),
        {k: v for k, v in final.items() if k != "confusion_matrix"},
        dataset_version=str(data_root.name),
    )
    print(f"\nRegistered waste-classifier-cnn {version} (status=staging).")
    print(f"Metrics report: {report_path}")
    print("Promote once you trust the numbers: ")
    print(f"  python -c \"from packages.ml.model_registry.registry import promote_to_production; "
          f"promote_to_production('waste-classifier-cnn', '{version}')\"")


if __name__ == "__main__":
    main()