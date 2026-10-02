"""In-process counters/timers — real, queryable via /api/v1/health or a
future /metrics endpoint. Swap for prometheus_client in production; this
keeps the interface dependency-free for the scaffold."""
import time
from collections import defaultdict
import threading

_lock = threading.Lock()
_counters: dict[str, int] = defaultdict(int)
_durations: dict[str, list[float]] = defaultdict(list)


def increment(name: str, amount: int = 1):
    with _lock:
        _counters[name] += amount


def record_duration(name: str, seconds: float):
    with _lock:
        _durations[name].append(seconds)


def snapshot() -> dict:
    with _lock:
        return {
            "counters": dict(_counters),
            "avg_duration_ms": {
                k: round((sum(v) / len(v)) * 1000, 2) for k, v in _durations.items() if v
            },
        }


class timed:
    """Context manager: `with timed('scan_inference'): ...`"""
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, *args):
        record_duration(self.name, time.time() - self._start)
