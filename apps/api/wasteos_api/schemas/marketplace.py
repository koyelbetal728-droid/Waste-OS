from pydantic import BaseModel
from typing import Optional


class ListingCreateRequest(BaseModel):
    material: str
    quantity_kg: float
    quality: Optional[str] = None
    contamination_level: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    waste_id: Optional[str] = None


class ListingResponse(BaseModel):
    id: str
    material: str
    quantity_kg: float
    quality: Optional[str]
    status: str
    price_min: Optional[float]
    price_max: Optional[float]

    class Config:
        from_attributes = True


class PurchaseRequest(BaseModel):
    listing_id: str


class TransactionResponse(BaseModel):
    id: str
    listing_id: str
    final_price: float

    class Config:
        from_attributes = True
