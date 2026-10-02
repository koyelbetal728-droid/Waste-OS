"""Shared dependency health checks — used by /api/v1/health and can be
reused by a readiness probe."""
from sqlalchemy import text


def check_database(db) -> bool:
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def check_redis() -> bool:
    try:
        import redis
        from packages.core.config import settings
        client = redis.Redis.from_url(settings.redis_url, socket_connect_timeout=2)
        return client.ping()
    except Exception:
        return False
