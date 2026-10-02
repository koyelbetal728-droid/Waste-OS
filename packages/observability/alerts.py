"""Alert dispatch stub — logs at ERROR level for now. Wire a real provider
(PagerDuty/Slack webhook) before relying on this in production; it never
silently swallows an alert."""
from packages.observability.logging import get_logger

logger = get_logger("alerts")


def fire_alert(name: str, details: dict):
    logger.error(f"ALERT: {name} | {details}")
