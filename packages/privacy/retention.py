"""Retention policy for personal data specifically (distinct from
packages/storage/retention.py, which handles raw files). Deletes audit log
rows older than the retention window — audit logs are append-only in
content but still subject to a retention limit."""
from datetime import datetime, timedelta
from packages.database.models.audit import AuditLog


def purge_old_audit_logs(db, days: int = 730) -> int:
    cutoff = datetime.utcnow() - timedelta(days=days)
    count = db.query(AuditLog).filter(AuditLog.created_at < cutoff).delete()
    db.commit()
    return count
