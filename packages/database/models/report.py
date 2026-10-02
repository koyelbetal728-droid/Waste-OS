import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base
import enum


class ReportStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"


class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)  # illegal_dumping | missed_pickup | overflow | hazardous | other
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(Enum(ReportStatus), default=ReportStatus.open)
    created_at = Column(DateTime, default=datetime.utcnow)
