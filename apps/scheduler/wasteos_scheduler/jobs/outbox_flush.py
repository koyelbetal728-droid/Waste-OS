"""Marks pending outbox events published — the scheduled counterpart to
apps/worker's on-demand outbox processor, for when nothing else is
triggering it."""
from packages.database.session import SessionLocal
from packages.database.models.outbox import OutboxEvent
from packages.observability.logging import get_logger

logger = get_logger("scheduler.outbox_flush")


def run():
    db = SessionLocal()
    try:
        pending = db.query(OutboxEvent).filter(OutboxEvent.published == False).limit(200).all()  # noqa: E712
        for event in pending:
            event.published = True
        db.commit()
        logger.info(f"Outbox flush: published {len(pending)} events")
    finally:
        db.close()
