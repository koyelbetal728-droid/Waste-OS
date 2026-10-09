"""Vision classifier interface.

Tries, in order:
  1. YoloDetectAdapter  — the real trained YOLOv11 detector (6 waste classes)
       registered as "waste-detector" in the model registry.
  2. RegistryAdapter    — the sklearn feature-based classifier (26 features /
       12 classes) when a production version is registered.
  3. MockClassifier     — a deterministic placeholder so the end-to-end pipeline
       still runs during early dev / until a real model is registered.

Each adapter returns the same ClassificationResult dataclass so the
classification pipeline (packages/ai/vision/pipeline.py) and the Celery
worker task don't care which backend produced the prediction.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
import hashlib
import os
import random

from packages.ml.model_registry.registry import get_production_model


@dataclass
class ClassificationResult:
    category: str
    material: str
    confidence: float
    contamination_level: str
    model_name: str
    model_version: str
    is_mock: bool


class BaseClassifier(ABC):
    @abstractmethod
    def predict(self, image_bytes: bytes) -> ClassificationResult:
        ...


# --------------------------------------------------------------------------- #
# 1) Real YOLOv11 detector
# --------------------------------------------------------------------------- #
# Maps the model's 6 detection classes to a recyclability "material" the
# domain engine (packages/waste/recyclability.py) understands, plus a
# human-readable category label for the UI.
_YOLO_CLASS_MATERIAL = {
    "plastic": "PET",
    "metal": "Aluminium",
    "glass": "Glass",
    "paper": "Paper",
    "cardboard": "Cardboard",
    "biodegradable": "Organic",
}


class YoloDetectAdapter(BaseClassifier):
    """Wraps the trained YOLOv11 detection model registered as
    "waste-detector". Raises RuntimeError (caught by get_classifier) when the
    model isn't registered / the artifact is missing, so the next adapter is
    tried."""

    _model = None
    _names: dict = {}
    _version: str = "unknown"

    def __init__(self):
        if YoloDetectAdapter._model is None:
            entry = get_production_model("waste-detector")
            if entry is None:
                raise RuntimeError("No production waste-detector registered yet.")
            artifact = entry["artifact_path"]
            if not os.path.exists(artifact):
                raise RuntimeError(f"YOLO model artifact not found: {artifact}")
            from ultralytics import YOLO as _YOLO  # heavy import, deferred

            YoloDetectAdapter._model = _YOLO(artifact)
            YoloDetectAdapter._names = YoloDetectAdapter._model.names or {}
            YoloDetectAdapter._version = entry["version"]
        self._model = YoloDetectAdapter._model
        self._names = YoloDetectAdapter._names
        self._version = YoloDetectAdapter._version

    @staticmethod
    def _contamination_for(conf: float) -> str:
        # Best-effort proxy: a high-confidence detection means the object was
        # cleanly isolated, so treat it as low contamination.
        return "low" if conf >= 0.6 else "medium"

    def predict(self, image_bytes: bytes) -> ClassificationResult:
        import io
        from PIL import Image

        results = self._model.predict(
            Image.open(io.BytesIO(image_bytes)),
            imgsz=640,
            conf=0.25,
            iou=0.45,
            verbose=False,
        )
        best_conf = 0.0
        best_class = None
        for r in results:
            for box in r.boxes:
                conf = float(box.conf.cpu().item())
                cls = int(box.cls.cpu().item())
                if conf > best_conf:
                    best_conf = conf
                    best_class = str(self._names.get(cls, "plastic")).lower()

        # No object met the detection threshold -> don't fabricate a class.
        # Returning a low-confidence "Unknown" lets the recyclability engine
        # come back as "unknown" instead of a confidently-wrong label.
        if best_conf < 0.05 or best_class is None:
            return ClassificationResult(
                category="Unknown",
                material="Unknown",
                confidence=round(best_conf, 4),
                contamination_level="unknown",
                model_name="waste-garbage-yolo11s",
                model_version=self._version,
                is_mock=False,
            )

        material = _YOLO_CLASS_MATERIAL.get(best_class, best_class.title())
        category = best_class.replace("_", " ").title()
        confidence = round(best_conf, 4)
        return ClassificationResult(
            category=category,
            material=material,
            confidence=confidence,
            contamination_level=self._contamination_for(confidence),
            model_name="waste-garbage-yolo11s",
            model_version=self._version,
            is_mock=False,
        )


# --------------------------------------------------------------------------- #
# 2) sklearn registry classifier adapter
# --------------------------------------------------------------------------- #
_SKLEARN_TO_MATERIAL = {
    "plastic": "PET",
    "metal": "Aluminium",
    "glass": "Glass",
    "paper": "Paper",
    "cardboard": "Cardboard",
    "biological": "Organic",
}


class RegistryAdapter(BaseClassifier):
    def __init__(self):
        entry = get_production_model("waste-classifier")
        if entry is None:
            raise RuntimeError("No production waste-classifier registered yet.")
        import pickle

        with open(entry["artifact_path"], "rb") as f:
            data = pickle.load(f)
        self.model = data["model"]
        self.class_names = data["class_names"]
        self.version = entry["version"]

    def predict(self, image_bytes: bytes) -> ClassificationResult:
        from packages.ml.classification.preprocessing import extract_features

        features = extract_features(image_bytes).reshape(1, -1)
        pred = str(self.model.predict(features)[0])
        proba = self.model.predict_proba(features)[0]
        confidence = float(max(proba))
        material = _SKLEARN_TO_MATERIAL.get(pred, pred)
        return ClassificationResult(
            category=pred.replace("_", " ").title(),
            material=material,
            confidence=round(confidence, 4),
            contamination_level="unknown",
            model_name="waste-classifier",
            model_version=self.version,
            is_mock=False,
        )


# --------------------------------------------------------------------------- #
# 3) Mock classifier (deterministic, dev-only)
# --------------------------------------------------------------------------- #
class MockClassifier(BaseClassifier):
    CATEGORIES = [
        ("Plastic Bottle", "PET"),
        ("Aluminium Can", "Aluminium"),
        ("Cardboard Box", "Cardboard"),
        ("Glass Jar", "Glass"),
        ("Mixed Waste", "Unknown"),
    ]
    CONTAMINATION = ["low", "medium", "high"]

    def predict(self, image_bytes: bytes) -> ClassificationResult:
        seed = int(hashlib.sha256(image_bytes).hexdigest(), 16) % (2 ** 32)
        rng = random.Random(seed)
        category, material = rng.choice(self.CATEGORIES)
        return ClassificationResult(
            category=category,
            material=material,
            confidence=round(rng.uniform(0.55, 0.97), 2),
            contamination_level=rng.choice(self.CONTAMINATION),
            model_name="mock-classifier",
            model_version="dev-0",
            is_mock=True,
        )


def get_classifier() -> BaseClassifier:
    """Returns the best available classifier."""
    for adapter in (YoloDetectAdapter, RegistryAdapter):
        try:
            return adapter()
        except RuntimeError:
            continue
    return MockClassifier()
