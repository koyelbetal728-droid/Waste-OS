import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from packages.database.base import Base
import enum


class ListingStatus(str, enum.Enum):
    active = "active"
    reserved = "reserved"
    sold = "sold"
    cancelled = "cancelled"


class Listing(Base):
    __tablename__ = "listings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    waste_id = Column(UUID(as_uuid=True), ForeignKey("waste.id"), nullable=True)

    material = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    quality = Column(String, nullable=True)          # e.g. "clean", "mixed"
    contamination_level = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    price_min = Column(Float, nullable=True)
    price_max = Column(Float, nullable=True)

    status = Column(Enum(ListingStatus), default=ListingStatus.active)
    verified = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    final_price = Column(Float, nullable=False)
    idempotency_key = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
