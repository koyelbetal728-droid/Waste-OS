from pydantic import BaseModel
from typing import Optional


class EWasteRequest(BaseModel):
    condition: Optional[str] = None  # working | minor_fault | major_fault | non_functional


class EWasteResponse(BaseModel):
    condition: Optional[str]
    pathway: str


class MedicalWasteRequest(BaseModel):
    category: Optional[str] = None


class MedicalWasteResponse(BaseModel):
    category: str
    requires_authorized_facility: bool
    recommended_action: str


class FoodWasteRequest(BaseModel):
    condition: Optional[str] = None
    hours_since_prep: Optional[float] = None


class FoodWasteResponse(BaseModel):
    eligible_for_donation: bool
    recommended_action: str
    reason: Optional[str] = None
