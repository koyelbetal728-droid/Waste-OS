import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base


class Ward(Base):
    __tablename__ = "wards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    name = Column(String, nullable=False)
    population = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
