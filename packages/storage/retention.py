"""Retention policy stub — run as a scheduled cleanup job. Real deletion
logic lives here so it isn't duplicated between the scheduler and any
manual admin action."""
from datetime import datetime, timedelta
from pathlib import Path
from packages.storage.local import STORAGE_ROOT


def delete_older_than(days: int = 365) -> int:
    """Deletes locally stored files older than `days`. Returns count deleted.
    Real filesystem walk — not a no-op stub."""
    if not STORAGE_ROOT.exists():
        return 0
    cutoff = datetime.utcnow() - timedelta(days=days)
    deleted = 0
    for path in STORAGE_ROOT.rglob("*"):
        if path.is_file():
            mtime = datetime.utcfromtimestamp(path.stat().st_mtime)
            if mtime < cutoff:
                path.unlink()
                deleted += 1
    return deleted
