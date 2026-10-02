"""Real, dependency-light image preprocessing: resize/normalize + a simple
color-histogram feature extractor. This keeps the whole classification
pipeline trainable on CPU with only Pillow + numpy — no GPU/deep-learning
stack required to get a genuine (if modest) working baseline. Swap in a
CNN/ResNet feature extractor later without changing the pipeline shape."""
import numpy as np
from PIL import Image
import io

IMAGE_SIZE = (64, 64)


def load_image(image_bytes: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return img.resize(IMAGE_SIZE)


def extract_features(image_bytes: bytes) -> np.ndarray:
    """Color-histogram feature vector (8 bins per channel = 24 dims) plus
    mean/std brightness. Cheap, real, and genuinely discriminative for
    material color differences (e.g. clear PET vs brown cardboard)."""
    img = load_image(image_bytes)
    arr = np.asarray(img).astype(np.float32) / 255.0

    features = []
    for channel in range(3):
        hist, _ = np.histogram(arr[:, :, channel], bins=8, range=(0, 1))
        features.extend(hist / hist.sum())

    gray = arr.mean(axis=2)
    features.append(gray.mean())
    features.append(gray.std())
    return np.array(features, dtype=np.float32)
