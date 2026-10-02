from wasteos_worker.celery_app import celery_app
from packages.database.session import SessionLocal
from packages.privacy.retention import purge_old_audit_logs


@celery_app.task(name="cleanup.expired_data")
def purge_expired_data():
    db = SessionLocal()
    try:
        return purge_old_audit_logs(db, days=730)
    finally:
        db.close()
