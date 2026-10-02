"""Shared image validation used before any vision inference — mirrors
packages/ml/classification/preprocessing.py but scoped to request-time
validation (file integrity, size) rather than feature extraction."""
from PIL import Image, UnidentifiedImageError
import io


def validate_image(image_bytes: bytes, max_dimension: int = 4096) -> tuple[bool, str | None]:
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()
    except UnidentifiedImageError:
        return False, "File is not a valid image."
    except Exception as e:
        return False, f"Image validation failed: {e}"

    img = Image.open(io.BytesIO(image_bytes))
    if max(img.size) > max_dimension:
        return False, f"Image exceeds max dimension of {max_dimension}px."
    return True, None
