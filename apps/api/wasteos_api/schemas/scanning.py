from pydantic import BaseModel
from typing import Optional
from .common import UUIDStr


class ScanJobResponse(BaseModel):
    job_id: UUIDStr
    waste_id: UUIDStr
    status: str


class ScanResultResponse(BaseModel):
    waste_id: UUIDStr
    status: str
    category: Optional[str] = None
    material: Optional[str] = None
    confidence: Optional[float] = None
    recyclability: Optional[str] = None
    contamination_level: Optional[str] = None
    hazard_level: Optional[str] = None
    estimated_value_min: Optional[float] = None
    estimated_value_max: Optional[float] = None
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    is_mock_model: bool = True
