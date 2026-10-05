"""Train the waste-object detector on the Roboflow garbage-detection dataset
(10,464 images, 6 classes: BIODEGRADABLE, CARDBOARD, GLASS, METAL, PAPER,
PLASTIC).

Get the data first — nothing under data/raw/ is committed:
    $env:ROBOFLOW_API_KEY="your-key"
    python -m scripts.fetch_datasets --detection
That script downloads the dataset and stages it onto local disk. The staging is
not optional politeness: a repo checked out inside OneDrive/Dropbox reads images
at 0.80 MB/s versus 54 MB/s on local disk, and the GPU then sits at 46W of a
~75W budget instead of loading up. It copies the data to
%LOCALAPPDATA%/wasteos-ml/data automatically.

Usage:
    python -m scripts.train_yolo_detect
    python -m scripts.train_yolo_detect --data-yaml "C:/waste-detect/data.yaml"
    python -m scripts.train_yolo_detect --resume-full \\
        models/artifacts/detect/<run>/weights/last.pt

Resuming — two different things, pick deliberately:
    --resume <ckpt>      load the weights only. Optimizer state, epoch counter
                         and LR schedule restart from scratch. Useful to branch
                         off a checkpoint with different hyperparameters; the
                         first few epochs will dip before recovering.
    --resume-full <ckpt> true continuation. Ultralytics restores optimizer,
                         epoch, best_fitness and the LR schedule position, so
                         training picks up exactly where it stopped. Use this to
                         finish an interrupted run.

Defaults target a 4GB laptop GPU (RTX 3050 class): yolo11s at 640, batch 8, AMP.
yolo11m/yolo11l at batch 16 need ~12GB+ VRAM and will OOM there.

Windows note: cap BLAS threads or the dataloader workers will exhaust the
system commit charge and die with "Unable to allocate 1.17 MiB":
    $env:OMP_NUM_THREADS="1"; $env:OPENBLAS_NUM_THREADS="1"; $env:MKL_NUM_THREADS="1"

Best weights land in models/artifacts/detect/<run>/weights/best.pt. Neither the
dataset nor the checkpoints are in git, so share last.pt separately (GitHub
Release asset or Git LFS) if someone else has to continue your run.
"""
import argparse
import hashlib
import os
import tempfile
from datetime import datetime
from pathlib import Path

from ultralytics import YOLO

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_YAML = (
    REPO_ROOT
    / "data"
    / "raw"
    / "waste"
    / "data"
    / "raw"
    / "detection"
    / "garbage_detection"
    / "GARBAGE CLASSIFICATION"
    / "data.yaml"
)
PROJECT_DIR = REPO_ROOT / "models" / "artifacts" / "detect"


def default_scratch() -> Path:
    override = os.environ.get("WASTE_ML_SCRATCH")
    if override:
        return Path(override)
    local = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return local / "wasteos-ml" / "data"


def candidate_data_yamls() -> list[Path]:
    env = os.environ.get("WASTE_DETECT_DATA_YAML")
    candidates = []
    if env:
        candidates.append(Path(env))
    candidates.append(default_scratch() / "waste-detect" / "data.yaml")
    candidates.append(default_scratch() / "GARBAGE CLASSIFICATION" / "data.yaml")
    candidates.append(Path("C:/waste-detect/data.yaml"))
    candidates.append(DATA_YAML)
    return candidates


def resolve_data_yaml(explicit: str) -> Path:
    if explicit:
        return Path(explicit)
    for candidate in candidate_data_yamls():
        if candidate.is_file():
            return candidate
    return DATA_YAML


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-yaml",
        default="",
        help="path to data.yaml (prefer a local non-OneDrive copy for speed)",
    )
    parser.add_argument("--model", default="yolo11s.pt")
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--device", default="0")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--patience", type=int, default=50)
    parser.add_argument("--close-mosaic", type=int, default=30)
    parser.add_argument("--cache", default="False", choices=["False", "ram", "disk"])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--name", default="waste-garbage-yolo11s")
    parser.add_argument(
        "--resume",
        default="",
        help="load weights from a checkpoint and restart optimizer/LR schedule",
    )
    parser.add_argument(
        "--resume-full",
        default="",
        help="true continuation: restore optimizer, epoch and LR schedule from a "
             "checkpoint, or pass 'auto' to pick the most recent committed one",
    )
    parser.add_argument(
        "--list-runs",
        action="store_true",
        help="list committed checkpoints and the exact --resume-full command for each",
    )
    parser.add_argument(
        "--checkpoint",
        default="",
        help="verify this checkpoint against its .sha256 before resuming",
    )
    return parser.parse_args()


def find_latest_checkpoint() -> Path | None:
    """Newest committed checkpoint under models/artifacts/detect/*/weights."""
    candidates = sorted(
        PROJECT_DIR.glob("*/weights/last.pt"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def list_runs() -> None:
    print(f"Detector runs under {PROJECT_DIR}:")
    found = False
    for ckpt in sorted(PROJECT_DIR.glob("*/weights/last.pt")):
        age = datetime.fromtimestamp(ckpt.stat().st_mtime)
        size_mb = ckpt.stat().st_size / 1e6
        print(f"  {ckpt.parent.parent.name:<40} {size_mb:5.1f} MB  {age:%Y-%m-%d %H:%M}")
        print(f"      continue with: --resume-full {ckpt}")
        found = True
    if not found:
        print("  (none — train one first, or the checkpoint was not committed)")


def main() -> None:
    args = parse_args()

    if args.checkpoint:
        ckpt = Path(args.checkpoint)
        if not ckpt.is_file():
            raise SystemExit(f"Checkpoint not found: {ckpt}")
        actual = hashlib.sha256(ckpt.read_bytes()).hexdigest()
        checksum_file = ckpt.with_suffix(ckpt.suffix + ".sha256")
        if checksum_file.is_file():
            expected = checksum_file.read_text(encoding="utf-8").split()[0].lower()
            if actual != expected:
                raise SystemExit(
                    f"Checksum mismatch for {ckpt}\n  expected {expected}\n  got      {actual}"
                )
            print(f"checksum ok: {actual[:16]}...")
        else:
            print(f"no .sha256 next to {ckpt}, skipping verification")

    if args.list_runs:
        list_runs()
        return

    if args.resume and args.resume_full:
        raise SystemExit("Use only one of --resume / --resume-full")

    if args.resume_full:
        target = args.resume_full
        if target.lower() == "auto":
            found = find_latest_checkpoint()
            if found is None:
                raise SystemExit(
                    f"No checkpoint found under {PROJECT_DIR}. Run --list-runs to see "
                    "what is available, or pass an explicit path."
                )
            target = str(found)
            print(f"Auto-selected most recent checkpoint: {target}")
        ckpt = Path(target)
        if not ckpt.is_file():
            raise SystemExit(f"Checkpoint not found: {ckpt}")

        data_yaml = resolve_data_yaml(args.data_yaml)
        if not data_yaml.is_file():
            raise SystemExit(
                f"No dataset config found (looked for {data_yaml}).\n"
                "Resume still needs the data. Run:\n"
                "  python -m scripts.fetch_datasets --detection"
            )

        model = YOLO(ckpt)
        print(f"Continuing {ckpt} (optimizer/epoch/LR schedule restored).")
        print(f"data: {data_yaml}")
        print("A committed checkpoint records the absolute data path of whichever")
        print("machine trained it. Ultralytics falls back to the data= value below")
        print("when that path does not exist here, so a clone on any other machine")
        print("resumes correctly against its own staged copy.")
        model.train(data=str(data_yaml), resume=True)
        print(f"\nBest weights: {ckpt.parent / 'best.pt'}")
        return

    data_yaml = resolve_data_yaml(args.data_yaml).resolve()
    if not data_yaml.exists():
        raise SystemExit(
            f"Dataset config not found: {data_yaml}\n"
            "Nothing under data/raw/ is committed. Get the data first:\n"
            "  $env:ROBOFLOW_API_KEY=\"your-key\"\n"
            "  python -m scripts.fetch_datasets --detection"
        )

    synced = any(m in str(data_yaml).lower() for m in ("onedrive", "dropbox", "googledrive"))
    if synced:
        print("WARNING: the dataset is inside a synced folder. Measured here: 0.80 MB/s")
        print("         read speed versus 54 MB/s on local disk, and the GPU then runs at")
        print("         46W of ~75W. Run scripts.fetch_datasets, which stages it to")
        print("         %LOCALAPPDATA%/wasteos-ml/data, then train against that.")

    missing = [
        split
        for split in ("train/images", "valid/images", "test/images")
        if not (data_yaml.parent / split).is_dir()
    ]
    if missing:
        raise SystemExit(
            "Missing split folders relative to data.yaml: " + ", ".join(missing)
        )

    PROJECT_DIR.mkdir(parents=True, exist_ok=True)

    model = YOLO(args.resume) if args.resume else YOLO(args.model)

    print(f"data:   {data_yaml}")
    print(f"model:  {args.model}  epochs={args.epochs}  imgsz={args.imgsz}  "
          f"batch={args.batch}  workers={args.workers}  cache={args.cache}")

    model.train(
        data=str(data_yaml),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        workers=args.workers,
        amp=True,
        project=str(PROJECT_DIR),
        name=args.name,
        exist_ok=True,
        seed=args.seed,
        deterministic=True,
        patience=args.patience,
        close_mosaic=args.close_mosaic,
        cos_lr=True,
        val=True,
        plots=True,
        cache=args.cache,
    )

    best = PROJECT_DIR / args.name / "weights" / "best.pt"
    print(f"\nBest weights: {best}")


if __name__ == "__main__":
    main()