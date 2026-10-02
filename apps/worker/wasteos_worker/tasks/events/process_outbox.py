from wasteos_worker.celery_app import celery_app
from packages.database.session import SessionLocal
from packages.database.models.outbox import OutboxEvent


@celery_app.task(name="events.process_outbox")
def process_outbox():
    db = SessionLocal()
    try:
        pending = db.query(OutboxEvent).filter(OutboxEvent.published == False).limit(100).all()  # noqa: E712
        for event in pending:
            # TODO: dispatch to real consumers (notifications, analytics, etc.)
            event.published = True
        db.commit()
    finally:
        db.close()
