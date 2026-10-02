from sqlalchemy.orm import Session
from packages.database.models.outbox import OutboxEvent


def publish_event(db: Session, event_type: str, payload: dict) -> OutboxEvent:
    """Write within the same DB transaction as the business change.
    A separate worker (apps/worker tasks/events/process_outbox.py) marks these published."""
    event = OutboxEvent(event_type=event_type, payload=payload)
    db.add(event)
    return event
