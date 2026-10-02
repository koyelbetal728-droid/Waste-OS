"""Loads the current PRODUCTION model from the registry, if one has been
trained and promoted. This is what packages/ai/vision/classifier.py should
be pointed at once you have a real trained model — see get_classifier()
there, which currently returns MockClassifier because nothing has been
registered/promoted yet."""
import pickle
from packages.ml.model_registry.registry import get_production_model
from packages.ml.classification.preprocessing import extract_features


class RegistryClassifier:
    """Real inference against a trained+promoted scikit-learn model."""

    def __init__(self):
        entry = get_production_model("waste-classifier")
        if entry is None:
            raise RuntimeError(
                "No production waste-classifier registered yet. Run "
                "`python -m packages.ml.classification.train` with images under "
                "data/raw/waste/<category>/, then promote the resulting version."
            )
        with open(entry["artifact_path"], "rb") as f:
            payload = pickle.load(f)
        self.model = payload["model"]
        self.class_names = payload["class_names"]
        self.version = entry["version"]
        self.metrics = entry["metrics"]

    def predict(self, image_bytes: bytes) -> dict:
        features = extract_features(image_bytes).reshape(1, -1)
        pred = self.model.predict(features)[0]
        proba = self.model.predict_proba(features)[0]
        confidence = float(max(proba))
        return {
            "category": pred,
            "confidence": confidence,
            "model_name": "waste-classifier",
            "model_version": self.version,
        }
