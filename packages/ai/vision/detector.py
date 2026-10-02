"""Object detection interface. No trained detector is bundled (that needs a
YOLO-class model + labeled bounding-box data this environment can't
produce) — this returns a single conservative "unknown region" whole-image
box so the API contract is real and stable today, and a real detector can
be dropped in later without changing callers."""
from dataclasses import dataclass


@dataclass
class Detection:
    label: str
    confidence: float
    bbox: tuple[float, float, float, float]  # x_min, y_min, x_max, y_max (normalized 0-1)


def detect_objects(image_bytes: bytes) -> list[Detection]:
    # No detector model registered yet — treat the whole frame as one region
    # rather than fabricating multiple fake bounding boxes.
    return [Detection(label="unclassified_region", confidence=0.0, bbox=(0.0, 0.0, 1.0, 1.0))]
