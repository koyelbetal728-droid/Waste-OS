import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base
import enum


class OrgType(str, enum.Enum):
    municipality = "municipality"
    recycler = "recycler"
    business = "business"
    facility = "facility"


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(Enum(OrgType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
