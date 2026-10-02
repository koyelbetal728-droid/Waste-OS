"""Dataset loader. Expects data/raw/waste/<category>/*.jpg — one folder per
class, matching TrashNet/TACO-style layout. Validates readability before
returning; skips (and reports) corrupt files rather than crashing training."""
from pathlib import Path
from dataclasses import dataclass
import numpy as np
from packages.ml.classification.preprocessing import extract_features

DATA_ROOT = Path(__file__).resolve().parents[3] / "data" / "raw" / "waste"


@dataclass
class Dataset:
    features: np.ndarray
    labels: list[str]
    class_names: list[str]
    skipped_files: list[str]


def load_dataset() -> Dataset:
    if not DATA_ROOT.exists():
        return Dataset(np.empty((0, 26)), [], [], [])

    class_dirs = sorted([d for d in DATA_ROOT.iterdir() if d.is_dir()])
    features, labels, skipped = [], [], []

    for class_dir in class_dirs:
        for img_path in class_dir.glob("*"):
            if img_path.suffix.lower() not in (".jpg", ".jpeg", ".png"):
                continue
            try:
                feat = extract_features(img_path.read_bytes())
                features.append(feat)
                labels.append(class_dir.name)
            except Exception:
                skipped.append(str(img_path))

    class_names = sorted(set(labels))
    feature_matrix = np.stack(features) if features else np.empty((0, 26))
    return Dataset(feature_matrix, labels, class_names, skipped)
