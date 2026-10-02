"""Re-exports the real distributed lock for cache-invalidation use cases
(e.g. only one process refreshes a cold cache key at a time)."""
from packages.locking.distributed_lock import DistributedLock, LockUnavailable  # noqa: F401
