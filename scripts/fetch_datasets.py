"""Fetch and stage the datasets this repo trains on, then print the exact
training command to run.

Nothing under data/raw/ is committed to git (see .gitignore), so a fresh clone
has no data. This script obtains the datasets two ways:

1. Roboflow export (preferred, keeps upstream canonical):
       export ROBOFLOW_API_KEY=xxxx   (Windows: $env:ROBOFLOW_API_KEY="xxxx")
       python -m scripts.fetch_datasets --detection
   Downloads version 2 of material-identification/garbage-classification-3 in
   YOLO format and verifies the split counts.

2. A prebuilt archive URL, for when no Roboflow key is available:
       python -m scripts.fetch_datasets --detection --archive-url <zip-url>
   Any zip containing train/valid/test + data.yaml works.

Staging (this matters more than it looks):
    The dataset is downloaded into the repo by default, which on a OneDrive or
    Dropbox-synced checkout means every one of the 10464 image reads goes
    through a filesystem filter. Measured on this machine: 0.80 MB/s there vs
    54 MB/s on local disk, and the GPU sat at 46W of a ~75W budget instead of
    loading up. So by default everything is staged to a local scratch directory
    outside any synced folder, and training is pointed at that copy.

    Override the location with WASTE_ML_SCRATCH, or --scratch.
    Pass --no-stage to keep it inside the repo anyway.

Classification data (garbage_classification, 12 classes, 15515 images) is a
separate download and has no public direct URL; pass --classification-data with
a path or archive URL if you have one. Training it needs far less throughput,
so the repo copy is usually fine for that one.
"""
import argparse
import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

DETECTION_ROBOFLOW = {
    "workspace": "material-identification",
    "project": "garbage-classification-3",
    "version": 2,
}
DETECTION_CLASSES = ["BIODEGRADABLE", "CARDBOARD", "GLASS", "METAL", "PAPER", "PLASTIC"]
DETECTION_EXPECTED = {"train": 7324, "valid": 2098, "test": 1042}

SYNCED_MARKERS = ("onedrive", "dropbox", "google drive", "googledrive", "icloud")

REPO_DETECTION_DIR = (
    REPO_ROOT / "data" / "raw" / "waste" / "data" / "raw" / "detection"
    / "garbage_detection" / "GARBAGE CLASSIFICATION"
)
REPO_CLASSIFICATION_DIR = (
    REPO_ROOT / "data" / "raw" / "waste" / "data" / "raw" / "waste"
    / "garbage_classification"
)


def default_scratch() -> Path:
    override = os.environ.get("WASTE_ML_SCRATCH")
    if override:
        return Path(override)
    local = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return local / "wasteos-ml" / "data"


def is_synced(path: Path) -> bool:
    lowered = str(path).lower()
    return any(marker in lowered for marker in SYNCED_MARKERS)


def download(url: str, dest: Path, timeout: int = 1800) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url}\n  -> {dest}")
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url, timeout=timeout) as response, tmp.open("wb") as out:
        total = response.headers.get("Content-Length")
        total_i = int(total) if total else 0
        read = 0
        while chunk := response.read(1 << 20):
            out.write(chunk)
            read += len(chunk)
            if total_i:
                pct = 100 * read / total_i
                print(f"\r  {read / 1e6:,.0f} / {total_i / 1e6:,.0f} MB ({pct:.0f}%)", end="")
    tmp.replace(dest)
    if total_i:
        print()


def _find_data_yaml(root: Path, max_depth: int = 3) -> Path | None:
    """Locate data.yaml anywhere near the top of an extracted tree."""
    if (root / "data.yaml").is_file():
        return root / "data.yaml"
    if max_depth <= 0:
        return None
    for child in sorted(p for p in root.iterdir() if p.is_dir()):
        found = _find_data_yaml(child, max_depth - 1)
        if found is not None:
            return found
    return None


def _promote(target: Path, source: Path) -> None:
    """Move everything in `source` up into `target`, then drop `source`."""
    for item in list(source.iterdir()):
        destination = target / item.name
        if destination.exists():
            if destination.is_dir():
                shutil.rmtree(destination)
            else:
                destination.unlink()
        shutil.move(str(item), str(destination))
    shutil.rmtree(source)


def _flatten_to_data_yaml(target: Path) -> None:
    """Make `target/data.yaml` valid regardless of how the archive was packed.

    Zip layouts vary: files at the root, everything under one named folder, or a
    folder per split with no top-level data.yaml at all. Walk down until
    data.yaml appears, then promote that directory's contents to the target.
    """
    for _ in range(4):
        if (target / "data.yaml").is_file():
            return
        found = _find_data_yaml(target)
        if found is None:
            return
        _promote(target, found.parent)


def extract(archive: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    print(f"Extracting {archive.name} -> {target}")
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(target)
    _flatten_to_data_yaml(target)


def roboflow_export_url(api_key: str, fmt: str = "yolov11") -> str:
    d = DETECTION_ROBOFLOW
    return (
        f"https://app.roboflow.com/{d['workspace']}/{d['project']}/{d['version']}"
        f"/export?api_key={api_key}&format={fmt}&split=all"
    )


def verify_detection(root: Path) -> bool:
    yaml_path = root / "data.yaml"
    if not yaml_path.exists():
        print(f"  FAIL: no data.yaml in {root}")
        return False

    ok = True
    for split, expected in DETECTION_EXPECTED.items():
        images = list((root / split / "images").glob("*")) if (root / split / "images").is_dir() else []
        labels = list((root / split / "labels").glob("*")) if (root / split / "labels").is_dir() else []
        status = "ok" if len(images) == expected else "MISMATCH"
        if len(images) != expected:
            ok = False
        print(f"  {split:<6} images={len(images):<6} labels={len(labels):<6} expected={expected:<6} {status}")

    text = yaml_path.read_text(encoding="utf-8", errors="ignore")
    missing = [c for c in DETECTION_CLASSES if c not in text]
    if missing:
        print(f"  FAIL: classes missing from data.yaml: {missing}")
        ok = False
    else:
        print(f"  classes ok: {', '.join(DETECTION_CLASSES)}")
    return ok


def stage(source: Path, scratch: Path, stage_it: bool) -> Path:
    if not stage_it:
        return source
    if not is_synced(source):
        print(f"  already off any synced folder: {source}")
        return source
    dest = scratch / source.name
    if dest.exists() and verify_detection_quiet(dest):
        print(f"  already staged: {dest}")
        return dest
    print(f"  staging off the synced folder to speed up training")
    print(f"    from {source}")
    print(f"    to   {dest}")
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest)
    print(f"  staged {sum(1 for _ in dest.rglob('*') if _.is_file()):,} files")
    return dest


def verify_detection_quiet(root: Path) -> bool:
    return (root / "data.yaml").exists() and all(
        (root / split / "images").is_dir() for split in DETECTION_EXPECTED
    )


def fetch_detection(args, scratch: Path) -> Path | None:
    repo_copy = REPO_DETECTION_DIR
    if verify_detection_quiet(repo_copy):
        print("Detection dataset already present in the repo:")
        print(f"  {repo_copy}")
        if not verify_detection(repo_copy):
            print("  FAIL: the copy in the repo does not match the expected splits.")
            print("  Expected 7324 train / 2098 valid / 1042 test and 6 class names.")
            print("  Re-fetch into a scratch dir and train from there:")
            print("    python -m scripts.fetch_datasets --detection --archive-url <zip-url>")
            return None
        return stage(repo_copy, scratch, args.stage)

    target = scratch / "waste-detect"
    if args.archive_url:
        archive = scratch / "detection.zip"
        download(args.archive_url, archive)
        extract(archive, target)
    else:
        api_key = os.environ.get("ROBOFLOW_API_KEY", "").strip()
        if not api_key:
            print(
                "No dataset found and no ROBOFLOW_API_KEY set.\n"
                "  Option A:  $env:ROBOFLOW_API_KEY=\"your-key\"  then re-run\n"
                "  Option B:  python -m scripts.fetch_datasets --detection "
                "--archive-url <a zip containing train/ valid/ test/ data.yaml>"
            )
            return None
        print(f"Exporting {DETECTION_ROBOFLOW['project']} v{DETECTION_ROBOFLOW['version']} from Roboflow")
        archive = scratch / "detection.zip"
        last_error = None
        for fmt in ("yolov11", "yolov8"):
            try:
                download(roboflow_export_url(api_key, fmt), archive)
                last_error = None
                break
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                print(f"  {fmt} export failed: {exc}")
        if last_error is not None:
            print("Roboflow export failed. Check the API key and that the "
                  "project is public or shared with your account.")
            return None
        extract(archive, target)

    print("Verifying downloaded detection dataset:")
    if not verify_detection(target):
        print("Downloaded dataset failed verification. Refusing to point training at it,")
        print("because a partial dataset silently trains a model against the wrong data.")
        return None
    if args.stage:
        repo_copy.parent.mkdir(parents=True, exist_ok=True)
        if not repo_copy.exists():
            shutil.copytree(target, repo_copy)
        print(f"  also saved into the repo at {repo_copy}")
    return target


def fetch_classification(args, scratch: Path) -> Path | None:
    repo_copy = REPO_CLASSIFICATION_DIR
    if repo_copy.is_dir():
        classes = [d for d in repo_copy.iterdir() if d.is_dir()]
        total = sum(len(list(d.glob("*"))) for d in classes)
        print(f"Classification data already present: {total:,} images across "
              f"{len(classes)} classes at {repo_copy}")
        if total < 100:
            print("  WARNING: that looks too small to train on")
        return repo_copy

    source = Path(args.classification_data) if args.classification_data else None
    if source is None and args.classification_url:
        archive = scratch / "classification.zip"
        download(args.classification_url, archive)
        target = scratch / "waste-classification"
        extract(archive, target)
        source = target
    if source is None:
        print("Classification dataset is not in this repo and no source given.")
        print("  Put one folder per class anywhere and pass --classification-data <path>,")
        print("  or set WASTE_CLASSIFICATION_DATA_ROOT. 12 classes expected:")
        print("  battery biological brown-glass cardboard clothes green-glass")
        print("  metal paper plastic shoes trash white-glass")
        print(f"  (this machine had it at {repo_copy} — copy it across, or re-download from")
        print("   Kaggle's 'garbage classification' dataset and regroup into those folders)")
        return None

    classes = [d for d in source.iterdir() if d.is_dir()]
    print(f"Classification data: {sum(len(list(d.glob('*'))) for d in classes):,} images "
          f"across {len(classes)} classes at {source}")
    return stage(source, scratch, args.stage)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--detection", action="store_true", help="fetch the YOLO detection set")
    parser.add_argument("--classification", action="store_true", help="check/locate the classification set")
    parser.add_argument("--all", action="store_true", help="both")
    parser.add_argument("--archive-url", default="", help="zip URL for the detection set")
    parser.add_argument("--classification-url", default="", help="zip URL for the classification set")
    parser.add_argument("--classification-data", default="", help="local folder, one dir per class")
    parser.add_argument("--scratch", default="", help="local scratch dir (default: %%LOCALAPPDATA%%/wasteos-ml/data)")
    parser.add_argument(
        "--no-stage",
        dest="stage",
        action="store_false",
        help="do not copy off synced folders (slower training)",
    )
    parser.set_defaults(stage=True)
    args = parser.parse_args()

    if not (args.detection or args.classification or args.all):
        parser.error("pick at least one of --detection / --classification / --all")

    scratch = Path(args.scratch) if args.scratch else default_scratch()
    scratch.mkdir(parents=True, exist_ok=True)

    repo_scratch = is_synced(REPO_ROOT)
    print(f"Repo:    {REPO_ROOT}")
    print(f"Scratch: {scratch}")
    if repo_scratch and args.stage:
        print("Note: the repo is inside a synced folder; data will be staged to "
              "local disk because reads through OneDrive/Dropbox are ~60x slower "
              "and starve the GPU.")

    detection_root = None
    if args.detection or args.all:
        print("\n=== detection (YOLO) ===")
        detection_root = fetch_detection(args, scratch)

    if args.classification or args.all:
        print("\n=== classification ===")
        fetch_classification(args, scratch)

    print("\n=== next steps ===")
    if detection_root:
        data_yaml = detection_root / "data.yaml"
        print("Detect objects (--workers defaults to auto, sized to this machine):")
        print(f'  python -m scripts.train_yolo_detect --data-yaml "{data_yaml}"')
        print("Continue an interrupted run from its committed checkpoint:")
        print(f'  python -m scripts.train_yolo_detect --data-yaml "{data_yaml}" --resume-full auto')
    else:
        print("Detection dataset unavailable — see the errors above. Without it there is")
        print("nothing to train; the committed checkpoint is only useful against the same")
        print("images. Either get a Roboflow API key, or share a zip with --archive-url.")
    print("Classify waste type:")
    print("  python -m packages.ml.classification.train")
    print("  python -m scripts.train_cnn_classifier")

    if detection_root is None and not (args.classification or args.all):
        sys.exit(1)


if __name__ == "__main__":
    main()