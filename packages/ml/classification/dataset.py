"""Dataset loader. Expects one folder per class containing *.jpg, matching
TrashNet/TACO-style layout. Validates readability before returning; skips (and
reports) corrupt files rather than crashing training.

The bundled raw dump nests the real class folders several levels down
(data/raw/waste/data/raw/waste/<class>/*.jpg) and also contains
`standardized_256` / `standardized_384`, which are resized copies of
`original` — feeding all three in would triple-count the same photos, so
DATA_ROOT points at the single canonical folder. Override with
WASTE_CLASSIFICATION_DATA_ROOT.
"""
import os
from pathlib import Path
from dataclasses import dataclass
import numpy as np
from packages.ml.classification.preprocessing import extract_features

_WASTE_ROOT = Path(__file__).resolve().parents[3] / "data" / "raw" / "waste"

DEFAULT_DATA_ROOT = _WASTE_ROOT / "data" / "raw" / "waste" / "garbage_classification"

FALLBACK_ROOTS = [
    DEFAULT_DATA_ROOT,
    _WASTE_ROOT / "data" / "raw" / "waste" / "original",
    _WASTE_ROOT / "data" / "raw" / "waste" / "Garbage classification" / "Garbage classification",
    _WASTE_ROOT,
]


@dataclass
class Dataset:
    features: np.ndarray
    labels: list[str]
    class_names: list[str]
    skipped_files: list[str]


def resolve_data_root() -> Path:
    override = os.environ.get("WASTE_CLASSIFICATION_DATA_ROOT")
    if override:
        return Path(override)
    for candidate in FALLBACK_ROOTS:
        if candidate.is_dir() and any(d.is_dir() for d in candidate.iterdir()):
            return candidate
    return DEFAULT_DATA_ROOT


def load_dataset(data_root: Path | None = None) -> Dataset:
    root = data_root or resolve_data_root()
    if not root.exists():
        return Dataset(np.empty((0, 26)), [], [], [])

    class_dirs = sorted([d for d in root.iterdir() if d.is_dir()])
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
