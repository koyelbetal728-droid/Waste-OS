import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base
import enum


class FacilityType(str, enum.Enum):
    recycler_facility = "recycler_facility"
    collection_point = "collection_point"
    processing_facility = "processing_facility"


class Facility(Base):
    __tablename__ = "facilities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    name = Column(String, nullable=False)
    type = Column(Enum(FacilityType), nullable=False)
    accepted_materials = Column(String, nullable=True)  # comma-separated, e.g. "PET,Aluminium,Glass"
    capacity_kg = Column(Float, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    operational = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
