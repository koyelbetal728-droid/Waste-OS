import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base
from packages.core.enums import WasteLifecycleStage, ScanStatus, RecyclabilityStatus


class Waste(Base):
    __tablename__ = "waste"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    category = Column(String, nullable=True)
    material = Column(String, nullable=True)
    quantity_kg = Column(Float, nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    lifecycle_stage = Column(Enum(WasteLifecycleStage), default=WasteLifecycleStage.created)
    scan_status = Column(Enum(ScanStatus), default=ScanStatus.queued)
    recyclability = Column(Enum(RecyclabilityStatus), default=RecyclabilityStatus.unknown)

    contamination_level = Column(String, nullable=True)
    hazard_level = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    model_name = Column(String, nullable=True)
    model_version = Column(String, nullable=True)

    image_path = Column(String, nullable=True)
    raw_ai_output = Column(JSON, nullable=True)

    estimated_value_min = Column(Float, nullable=True)
    estimated_value_max = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
