import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base
import enum


class VehicleStatus(str, enum.Enum):
    available = "available"
    on_route = "on_route"
    maintenance = "maintenance"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    label = Column(String, nullable=False)          # e.g. plate number
    capacity_kg = Column(Float, nullable=True)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.available)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
