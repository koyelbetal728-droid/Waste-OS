"""Async wrapper around the same detection logic the API/scheduler use —
lets the API queue detection instead of running it synchronously if report
volume grows large enough to matter."""
from wasteos_worker.celery_app import celery_app
from packages.database.session import SessionLocal
from packages.database.models.hotspot import Hotspot
from packages.database.models.report import Report
from packages.geospatial.hotspot import detect_hotspots


@celery_app.task(name="geospatial.detect_hotspots")
def detect_hotspots_task():
    db = SessionLocal()
    try:
        reports = db.query(Report).filter(Report.latitude.isnot(None)).all()
        points = [{"latitude": r.latitude, "longitude": r.longitude} for r in reports]
        clusters = detect_hotspots(points)
        for c in clusters:
            db.add(Hotspot(**c))
        db.commit()
        return len(clusters)
    finally:
        db.close()
