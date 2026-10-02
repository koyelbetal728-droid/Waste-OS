"""Email delivery interface. No SMTP/SES/SendGrid credentials exist in
this environment — send() logs and returns a clear 'not_configured' status
rather than pretending an email went out. Wire a real provider before
relying on this."""
from packages.observability.logging import get_logger

logger = get_logger("notifications.email")


def send(to_email: str, subject: str, body: str) -> dict:
    logger.info(f"[EMAIL NOT CONFIGURED] Would send to {to_email}: {subject}")
    return {"status": "not_configured", "channel": "email"}
