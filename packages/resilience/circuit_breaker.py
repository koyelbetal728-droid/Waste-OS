"""Minimal in-process circuit breaker. Opens after `failure_threshold`
consecutive failures and stays open for `reset_seconds` before allowing a
trial call through again. Real state machine, not a stub."""
import time


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_seconds: float = 30.0):
        self.failure_threshold = failure_threshold
        self.reset_seconds = reset_seconds
        self.failure_count = 0
        self.opened_at: float | None = None

    def _is_open(self) -> bool:
        if self.opened_at is None:
            return False
        if time.time() - self.opened_at > self.reset_seconds:
            self.opened_at = None
            self.failure_count = 0
            return False
        return True

    def call(self, fn, *args, **kwargs):
        if self._is_open():
            raise CircuitOpenError("Circuit is open — too many recent failures.")
        try:
            result = fn(*args, **kwargs)
            self.failure_count = 0
            return result
        except Exception:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.opened_at = time.time()
            raise
