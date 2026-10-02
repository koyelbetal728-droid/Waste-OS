"""Push notification interface. No FCM/APNs credentials exist in this
environment — same honest 'not_configured' behavior as email.py."""
from packages.observability.logging import get_logger

logger = get_logger("notifications.push")


def send(user_id: str, title: str, body: str) -> dict:
    logger.info(f"[PUSH NOT CONFIGURED] Would notify user {user_id}: {title}")
    return {"status": "not_configured", "channel": "push"}
