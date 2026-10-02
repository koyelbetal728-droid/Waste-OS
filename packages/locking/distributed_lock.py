"""Public entry point — callers import from here, not redis_lock.py
directly, so the backend can change without touching call sites."""
from packages.locking.redis_lock import DistributedLock, LockUnavailable  # noqa: F401
