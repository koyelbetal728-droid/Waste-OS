"""Image-modality entry point used by the orchestrator."""
from packages.ai.vision.preprocessing import validate_image
from packages.ai.vision.classifier import get_classifier


def process_image(image_bytes: bytes) -> dict:
    valid, error = validate_image(image_bytes)
    if not valid:
        return {"status": "invalid", "error": error}
    result = get_classifier().predict(image_bytes)
    return {
        "status": "ok",
        "category": result.category,
        "material": result.material,
        "confidence": result.confidence,
        "contamination_level": result.contamination_level,
        "is_mock": result.is_mock,
    }
