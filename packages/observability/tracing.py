"""Minimal span tracking — records nested operation timings per request via
the same contextvar as correlation.py. Not a full OpenTelemetry
integration; wire that in before relying on this for production tracing."""
import time
from packages.observability.metrics import record_duration


class Span:
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, *args):
        record_duration(f"span.{self.name}", time.time() - self._start)
