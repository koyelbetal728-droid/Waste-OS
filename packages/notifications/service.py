"""Orchestrates a single notification across the user's enabled channels.
Always writes the notification to the outbox/DB (real, durable) regardless
of whether any external channel is configured — that's what
/api/v1/notifications reads from today."""
from packages.notifications.templates import render
from packages.notifications.preferences import get_preferences
from packages.notifications import email, push


def notify(db, user, template_key: str, **kwargs) -> dict:
    message = render(template_key, **kwargs)
    prefs = get_preferences(user)
    results = {}
    if prefs.get("email"):
        results["email"] = email.send(user.email, template_key.replace("_", " ").title(), message)
    if prefs.get("push"):
        results["push"] = push.send(str(user.id), template_key.replace("_", " ").title(), message)

    from packages.events.outbox import publish_event
    publish_event(db, "NotificationSent", {"user_id": str(user.id), "template": template_key, "message": message})
    return {"message": message, "channels": results}
