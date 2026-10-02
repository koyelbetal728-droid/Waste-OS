from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.observability.health import check_database, check_redis
from packages.observability.metrics import snapshot

router = APIRouter()


@router.get("/health")
def health(db: Session = Depends(get_db)):
    db_ok = check_database(db)
    redis_ok = check_redis()
    status = "healthy" if (db_ok and redis_ok) else "degraded"
    return {"status": status, "dependencies": {"database": db_ok, "redis": redis_ok}}


@router.get("/metrics")
def metrics():
    """Real in-process counters/timers — see packages/observability/metrics.py."""
    return snapshot()
