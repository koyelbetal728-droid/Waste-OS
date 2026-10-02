from sqlalchemy.orm import Session
from packages.database.models.idempotency import IdempotencyKey


def get_cached_response(db: Session, key: str):
    row = db.query(IdempotencyKey).filter(IdempotencyKey.key == key).first()
    return row.response_body if row else None


def store_response(db: Session, key: str, endpoint: str, response_body: dict):
    row = IdempotencyKey(key=key, endpoint=endpoint, response_body=response_body)
    db.add(row)
