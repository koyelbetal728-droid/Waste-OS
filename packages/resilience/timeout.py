"""Simple timeout decorator wrapper for I/O calls (used by ollama_client
and any future external HTTP calls). Uses signal-based timeout on Unix."""
import functools
import signal


class TimeoutError_(Exception):
    pass


def with_timeout(seconds: float):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise TimeoutError_(f"{fn.__name__} exceeded {seconds}s timeout")
            old_handler = signal.signal(signal.SIGALRM, handler)
            signal.setitimer(signal.ITIMER_REAL, seconds)
            try:
                return fn(*args, **kwargs)
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
                signal.signal(signal.SIGALRM, old_handler)
        return wrapper
    return decorator
