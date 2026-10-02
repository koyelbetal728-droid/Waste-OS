"""Real cleanup job: purges old audit logs and stale local storage files."""
from packages.database.session import SessionLocal
from packages.privacy.retention import purge_old_audit_logs
from packages.storage.retention import delete_older_than
from packages.observability.logging import get_logger

logger = get_logger("scheduler.cleanup")


def run():
    db = SessionLocal()
    try:
        audit_deleted = purge_old_audit_logs(db, days=730)
        files_deleted = delete_older_than(days=365)
        logger.info(f"Cleanup: purged {audit_deleted} audit rows, {files_deleted} stored files")
    finally:
        db.close()
