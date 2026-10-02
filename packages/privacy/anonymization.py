"""Real anonymization — irreversibly scrambles PII fields in place rather
than just flagging a 'deleted' bool. Used by deletion.py; also usable
standalone for GDPR-style anonymize-but-keep-aggregates requests."""
import hashlib


def anonymize_user(user):
    salt = str(user.id)
    user.email = f"deleted-{hashlib.sha256((user.email + salt).encode()).hexdigest()[:12]}@deleted.local"
    user.full_name = "Deleted User"
    user.is_active = False
    return user
