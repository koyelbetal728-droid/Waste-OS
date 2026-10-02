"""Thin Redis client wrapper — one place to configure connection settings."""
import redis
from packages.core.config import settings

_client = None


def get_client() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.Redis.from_url(settings.redis_url, socket_connect_timeout=2, decode_responses=True)
    return _client
