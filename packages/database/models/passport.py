import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base


class Passport(Base):
    __tablename__ = "passports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    waste_id = Column(UUID(as_uuid=True), ForeignKey("waste.id"), nullable=False, unique=True)
    qr_token = Column(String, unique=True, default=lambda: uuid.uuid4().hex)
    events = Column(JSON, default=list)  # append-only list of {stage, timestamp, actor, metadata}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
