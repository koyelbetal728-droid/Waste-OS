from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.waste import Waste
from packages.database.models.report import Report, ReportStatus
from packages.database.models.hotspot import Hotspot
from packages.core.enums import RecyclabilityStatus
from wasteos_api.schemas.municipality import AnalyticsResponse

router = APIRouter()


@router.get("/analytics", response_model=AnalyticsResponse)
def analytics(db: Session = Depends(get_db)):
    total = db.query(Waste).count()
    recycled = db.query(Waste).filter(Waste.recyclability == RecyclabilityStatus.recyclable).count()
    open_reports = db.query(Report).filter(Report.status == ReportStatus.open).count()
    hotspots = db.query(Hotspot).count()
    return AnalyticsResponse(
        total_waste_records=total,
        recycled_count=recycled,
        recycling_rate=round((recycled / total) * 100, 1) if total else 0.0,
        open_reports=open_reports,
        active_hotspots=hotspots,
    )
