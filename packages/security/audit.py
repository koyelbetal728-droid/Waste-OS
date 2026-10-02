"""Writes append-only audit entries — callers pass the same db session as
the enclosing transaction so the audit row commits atomically with the
business change it's recording."""
from packages.database.models.audit import AuditLog


def write_audit(db, actor_id, action: str, target: str | None = None, metadata: dict | None = None):
    entry = AuditLog(actor_id=actor_id, action=action, target=target, metadata_json=metadata)
    db.add(entry)
    return entry
