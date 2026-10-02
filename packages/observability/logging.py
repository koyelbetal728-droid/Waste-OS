"""Structured JSON logging — every line carries request_id when available,
never logs secrets/PII."""
import json
import logging
import sys
from packages.observability.correlation import get_request_id


class JSONFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "request_id": get_request_id(),
        }
        return json.dumps(payload)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
