import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String, unique=True, nullable=False, index=True)
    endpoint = Column(String, nullable=False)
    response_body = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
