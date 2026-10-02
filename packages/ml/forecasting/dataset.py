"""Turns raw {date, quantity_kg} history into a feature matrix + target
vector for training. No temporal shuffling — a chronological split is used
in evaluate.py to avoid future-leakage."""
import numpy as np
from packages.ml.forecasting.features import build_features


def build_dataset(history: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for point in history:
        f = build_features(point["date"])
        X.append([f["weekday"], f["month"], f["is_weekend"]])
        y.append(point["quantity_kg"])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)
