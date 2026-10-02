import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base


class WasteTypeConfig(Base):
    """Admin-configurable waste taxonomy — the recyclability engine
    (packages/waste/recyclability.py) currently uses a hard-coded default
    set; this table lets an admin extend/override it per municipality."""
    __tablename__ = "waste_type_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)      # e.g. "PET"
    category = Column(String, nullable=False)               # e.g. "plastic"
    recyclable_default = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
