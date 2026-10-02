"""Real Redis-backed distributed lock using SET NX EX (atomic acquire).
Falls back to raising LockUnavailable rather than silently proceeding
without a lock if Redis is unreachable — a scheduled job should skip its
run, not risk running twice."""
import uuid
import redis
from packages.core.config import settings


class LockUnavailable(Exception):
    pass


_client = None


def _get_client():
    global _client
    if _client is None:
        _client = redis.Redis.from_url(settings.redis_url, socket_connect_timeout=2)
    return _client


class DistributedLock:
    def __init__(self, key: str, ttl_seconds: int = 60):
        self.key = f"lock:{key}"
        self.ttl_seconds = ttl_seconds
        self.token = str(uuid.uuid4())

    def acquire(self) -> bool:
        try:
            return bool(_get_client().set(self.key, self.token, nx=True, ex=self.ttl_seconds))
        except redis.RedisError as e:
            raise LockUnavailable(str(e))

    def release(self):
        try:
            client = _get_client()
            if client.get(self.key) == self.token.encode():
                client.delete(self.key)
        except redis.RedisError:
            pass  # best-effort release; TTL will expire it anyway

    def __enter__(self):
        if not self.acquire():
            raise LockUnavailable(f"Could not acquire lock: {self.key}")
        return self

    def __exit__(self, *args):
        self.release()
