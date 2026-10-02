"""Validates/normalizes client-supplied Idempotency-Key headers."""

MAX_KEY_LENGTH = 200


def is_valid_key(key: str | None) -> bool:
    if not key:
        return False
    return 0 < len(key) <= MAX_KEY_LENGTH
