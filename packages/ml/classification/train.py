"""Train a real (small, CPU-only) waste classifier: logistic regression over
color-histogram features. Honest about what it is — a genuine working
baseline, not a claimed state-of-the-art CNN. Swap the estimator for a
torchvision CNN later; dataset.py/evaluate.py/inference.py stay the same
shape.

Usage (inside the api/worker container, which has sklearn installed):
    python -m packages.ml.classification.train
"""
import pickle
from datetime import datetime
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from packages.ml.classification.dataset import load_dataset
from packages.ml.classification.evaluate import evaluate_model
from packages.ml.model_registry.registry import register_model

ARTIFACT_DIR = Path(__file__).resolve().parents[3] / "models" / "artifacts"


def train():
    dataset = load_dataset()
    if len(dataset.labels) < 10:
        print(f"Not enough data to train: found {len(dataset.labels)} images "
              f"under data/raw/waste/<category>/. Need at least 10 (ideally hundreds per class).")
        print("Populate data/raw/waste/<category>/*.jpg and re-run.")
        return None

    X_train, X_test, y_train, y_test = train_test_split(
        dataset.features, dataset.labels, test_size=0.2, random_state=42, stratify=dataset.labels
    )

    model = LogisticRegression(max_iter=1000, multi_class="auto")
    model.fit(X_train, y_train)

    metrics = evaluate_model(model, X_test, y_test, dataset.class_names)
    print("Evaluation metrics:", metrics)

    version = datetime.utcnow().strftime("v%Y%m%d%H%M%S")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    artifact_path = ARTIFACT_DIR / f"waste-classifier-{version}.pkl"
    with open(artifact_path, "wb") as f:
        pickle.dump({"model": model, "class_names": dataset.class_names}, f)

    register_model("waste-classifier", version, str(artifact_path), metrics)
    print(f"Registered waste-classifier {version}. Promote it with "
          f"packages.ml.model_registry.registry.promote_to_production('waste-classifier', '{version}') "
          f"once you're satisfied with the metrics above.")
    return version


if __name__ == "__main__":
    train()
