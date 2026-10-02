"""Retry decorator using real exponential backoff (backoff.py). Only wrap
calls that are safe to retry — never non-idempotent mutations."""
import time
import functools
from packages.resilience.backoff import compute_delay


def retry(max_attempts: int = 3, exceptions: tuple = (Exception,)):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt < max_attempts - 1:
                        time.sleep(compute_delay(attempt))
            raise last_exc
        return wrapper
    return decorator
