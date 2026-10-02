"""Real requeue logic: any waste record stuck in 'processing' for over an
hour (worker crash mid-task) gets reset to 'queued' so it can be retried,
instead of being silently stuck forever."""
from datetime import datetime, timedelta
from wasteos_worker.celery_app import celery_app
from packages.database.session import SessionLocal
from packages.database.models.waste import Waste
from packages.core.enums import ScanStatus


@celery_app.task(name="cleanup.requeue_stuck_scans")
def requeue_stuck_scans():
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(hours=1)
        stuck = db.query(Waste).filter(Waste.scan_status == ScanStatus.processing, Waste.updated_at < cutoff).all()
        for w in stuck:
            w.scan_status = ScanStatus.queued
        db.commit()
        return len(stuck)
    finally:
        db.close()
