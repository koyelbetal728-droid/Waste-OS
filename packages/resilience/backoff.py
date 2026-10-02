"""Exponential backoff delay calculator — pure function, easy to unit test."""


def compute_delay(attempt: int, base_seconds: float = 0.5, max_seconds: float = 30.0) -> float:
    return min(base_seconds * (2 ** attempt), max_seconds)
