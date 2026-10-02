import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base


class Hotspot(Base):
    """Simplified point-based hotspot (production should store real PostGIS
    geometry via db/postgis — this column-based version keeps the scaffold
    runnable without a spatial migration)."""
    __tablename__ = "hotspots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    severity = Column(String, default="low")   # low | medium | high
    report_count = Column(Integer, default=1)
    ward = Column(String, nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow)
