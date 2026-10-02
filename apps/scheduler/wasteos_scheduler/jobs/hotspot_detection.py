"""Real scheduled job — guarded by the same distributed lock the manual
API trigger uses, so a scheduled run and a manual run can never overlap."""
from packages.database.session import SessionLocal
from packages.database.models.hotspot import Hotspot
from packages.database.models.report import Report
from packages.geospatial.hotspot import detect_hotspots
from packages.locking.distributed_lock import DistributedLock, LockUnavailable
from packages.locking.lock_keys import HOTSPOT_DETECTION
from packages.observability.logging import get_logger

logger = get_logger("scheduler.hotspot_detection")


def run():
    try:
        with DistributedLock(HOTSPOT_DETECTION, ttl_seconds=60):
            db = SessionLocal()
            try:
                reports = db.query(Report).filter(Report.latitude.isnot(None)).all()
                points = [{"latitude": r.latitude, "longitude": r.longitude} for r in reports]
                clusters = detect_hotspots(points)
                for c in clusters:
                    db.add(Hotspot(**c))
                db.commit()
                logger.info(f"Hotspot detection: {len(clusters)} clusters found from {len(reports)} reports")
            finally:
                db.close()
    except LockUnavailable:
        logger.info("Skipped hotspot detection — already running elsewhere")
