import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base


class AuditLog(Base):
    """Append-only. Never updated or deleted by application code."""
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)   # e.g. "login", "user.role_changed"
    target = Column(String, nullable=True)    # e.g. "user:<id>"
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
