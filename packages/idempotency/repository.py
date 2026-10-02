"""Persistence layer for idempotency keys — service.py calls this rather
than querying the model directly, so the storage shape can change without
touching every endpoint that uses idempotency."""
from packages.database.models.idempotency import IdempotencyKey


def find_by_key(db, key: str) -> IdempotencyKey | None:
    return db.query(IdempotencyKey).filter(IdempotencyKey.key == key).first()


def create(db, key: str, endpoint: str, response_body: dict) -> IdempotencyKey:
    row = IdempotencyKey(key=key, endpoint=endpoint, response_body=response_body)
    db.add(row)
    return row
