"""Vision classifier interface.

IMPORTANT: This module ships a MockClassifier so the end-to-end pipeline
(upload -> queue -> worker -> result) runs without a trained model. It is
labeled clearly and its confidence/output must never be presented as a real
trained model's output. Swap `get_classifier()` for a real implementation
(ONNX/PyTorch) once packages/ml/classification/train.py has produced and
registered a validated artifact.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
import hashlib
import random


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


class MockClassifier(BaseClassifier):
    """Deterministic-per-image placeholder. NOT a trained model.
    Uses a hash of the image bytes purely so results are stable across repeated calls,
    not to imply any real visual understanding."""

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
    """Tries the real registry-loaded model first (see
    packages/ml/classification/inference.py). Falls back to MockClassifier
    only when nothing has been trained+promoted yet — never silently
    fabricates a "trained" result."""
    try:
        from packages.ml.classification.inference import RegistryClassifier
        registry_model = RegistryClassifier()

        class _RegistryAdapter(BaseClassifier):
            def predict(self, image_bytes: bytes) -> ClassificationResult:
                result = registry_model.predict(image_bytes)
                return ClassificationResult(
                    category=result["category"],
                    material=result["category"],
                    confidence=result["confidence"],
                    contamination_level="unknown",  # contamination needs a separate model/signal
                    model_name=result["model_name"],
                    model_version=result["model_version"],
                    is_mock=False,
                )
        return _RegistryAdapter()
    except RuntimeError:
        return MockClassifier()
