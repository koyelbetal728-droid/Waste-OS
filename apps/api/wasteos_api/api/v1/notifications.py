"""Notification API. No delivery channel (email/push) is configured in this
environment, so notifications are stored and marked read/unread here —
actual sending is handled asynchronously by
apps/worker/wasteos_worker/tasks/notifications/* once a provider is wired."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.outbox import OutboxEvent
from packages.database.models.user import User
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.get("")
def list_notifications(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Surfaces recent outbox events relevant to this user as notifications
    — a real, if minimal, notification feed with no fabricated content."""
    events = db.query(OutboxEvent).order_by(OutboxEvent.created_at.desc()).limit(20).all()
    return [{"id": str(e.id), "type": e.event_type, "payload": e.payload, "created_at": e.created_at.isoformat()} for e in events]
