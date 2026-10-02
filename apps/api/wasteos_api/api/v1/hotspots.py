from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.hotspot import Hotspot
from packages.database.models.report import Report
from packages.geospatial.hotspot import detect_hotspots
from packages.locking.distributed_lock import DistributedLock, LockUnavailable
from packages.locking.lock_keys import HOTSPOT_DETECTION

router = APIRouter()


@router.get("")
def list_hotspots(db: Session = Depends(get_db)):
    return db.query(Hotspot).order_by(Hotspot.detected_at.desc()).all()


@router.post("/detect", status_code=202)
def run_hotspot_detection(db: Session = Depends(get_db)):
    """Guarded by a real distributed lock so two concurrent calls (or a
    scheduled job overlapping a manual trigger) never double-run clustering."""
    try:
        lock = DistributedLock(HOTSPOT_DETECTION, ttl_seconds=30)
        if not lock.acquire():
            raise HTTPException(status_code=409, detail={"error": {"code": "DETECTION_IN_PROGRESS", "message": "Hotspot detection is already running."}})
    except LockUnavailable:
        raise HTTPException(status_code=503, detail={"error": {"code": "LOCK_SERVICE_UNAVAILABLE", "message": "Could not reach the locking service."}})

    try:
        reports = db.query(Report).filter(Report.latitude.isnot(None)).all()
        points = [{"latitude": r.latitude, "longitude": r.longitude} for r in reports]
        clusters = detect_hotspots(points)
        created = []
        for c in clusters:
            hotspot = Hotspot(**c)
            db.add(hotspot)
            created.append(c)
        db.commit()
        return {"detected": len(created), "hotspots": created}
    finally:
        lock.release()
