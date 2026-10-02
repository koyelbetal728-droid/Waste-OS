"""Storage facade — business logic never imports local.py/object_storage.py
directly, so switching backends never touches callers."""
import os
from packages.storage import local, object_storage

BACKEND = os.environ.get("STORAGE_BACKEND", "local")


def save_file(key_prefix: str, content: bytes, extension: str = "bin") -> str:
    if BACKEND == "local":
        return local.save(key_prefix, content, extension)
    return object_storage.save(key_prefix, content, extension)


def read_file(relative_path: str) -> bytes:
    if BACKEND == "local":
        return local.read(relative_path)
    raise NotImplementedError("Object storage read not implemented — no credentials configured.")
