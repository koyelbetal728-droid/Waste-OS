import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base
from packages.core.enums import PickupStatus


class Pickup(Base):
    __tablename__ = "pickups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    citizen_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    collector_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    waste_id = Column(UUID(as_uuid=True), ForeignKey("waste.id"), nullable=True)

    status = Column(Enum(PickupStatus), default=PickupStatus.requested)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    preferred_time = Column(DateTime, nullable=True)

    idempotency_key = Column(String, unique=True, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
