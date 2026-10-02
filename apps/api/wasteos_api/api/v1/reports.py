from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.report import Report
from packages.database.models.user import User
from packages.events.outbox import publish_event
from wasteos_api.schemas.municipality import ReportCreateRequest, ReportResponse
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.post("", response_model=ReportResponse, status_code=201)
def create_report(payload: ReportCreateRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    report = Report(reporter_id=user.id, **payload.model_dump())
    db.add(report)
    db.flush()
    publish_event(db, "ReportCreated", {"report_id": str(report.id), "category": report.category})
    db.commit()
    db.refresh(report)
    return report


@router.get("", response_model=list[ReportResponse])
def list_my_reports(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Report).filter(Report.reporter_id == user.id).order_by(Report.created_at.desc()).all()
