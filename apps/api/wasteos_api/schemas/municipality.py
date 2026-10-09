from pydantic import BaseModel
from typing import Optional
from .common import UUIDStr


class ReportCreateRequest(BaseModel):
    category: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ReportResponse(BaseModel):
    id: UUIDStr
    category: str
    status: str

    class Config:
        from_attributes = True


class HotspotResponse(BaseModel):
    id: UUIDStr
    latitude: float
    longitude: float
    severity: str
    report_count: int

    class Config:
        from_attributes = True


class AnalyticsResponse(BaseModel):
    total_waste_records: int
    recycled_count: int
    recycling_rate: float
    open_reports: int
    active_hotspots: int
