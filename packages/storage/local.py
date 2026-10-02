"""Real local-filesystem storage backend. Files land under STORAGE_ROOT
(configurable), keyed by a content-addressed-ish path so re-uploads of the
same bytes don't collide. This is what makes uploaded scan images
survive past the request — previously they were only ever held in memory
and passed straight to the Celery task."""
import hashlib
import os
from pathlib import Path

STORAGE_ROOT = Path(os.environ.get("STORAGE_ROOT", "/tmp/wasteos-storage"))


def save(key_prefix: str, content: bytes, extension: str = "bin") -> str:
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(content).hexdigest()[:16]
    relative_path = f"{key_prefix}/{digest}.{extension}"
    full_path = STORAGE_ROOT / relative_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if not full_path.exists():
        full_path.write_bytes(content)
    return relative_path


def read(relative_path: str) -> bytes:
    full_path = STORAGE_ROOT / relative_path
    if not full_path.exists():
        raise FileNotFoundError(relative_path)
    return full_path.read_bytes()


def delete(relative_path: str) -> None:
    full_path = STORAGE_ROOT / relative_path
    if full_path.exists():
        full_path.unlink()
