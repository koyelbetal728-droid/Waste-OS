import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base


class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
