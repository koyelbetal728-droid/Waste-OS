"""Object-storage interface. No S3/GCS credentials exist in this
environment, so this raises clearly rather than silently writing nowhere —
implement against boto3/gcs when you have real credentials. storage.py
picks this vs local.py based on config, so callers never need to know
which backend is active."""


class ObjectStorageNotConfigured(Exception):
    pass


def save(key_prefix: str, content: bytes, extension: str = "bin") -> str:
    raise ObjectStorageNotConfigured(
        "No object storage credentials configured. Set STORAGE_BACKEND=local "
        "(the default) or implement this against your S3/GCS provider."
    )
