"""Segmentation interface — optional, computationally heavier stage. No
trained segmentation model is bundled; returns None (caller must treat this
as "segmentation unavailable", never fabricate a mask)."""


def segment(image_bytes: bytes) -> None:
    return None
