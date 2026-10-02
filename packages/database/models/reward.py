import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base


class Reward(Base):
    """Append-only ledger entry — never overwrite a balance directly."""
    __tablename__ = "rewards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    points = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)  # e.g. "pickup_verified", "correct_segregation"
    reference_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
