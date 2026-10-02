"""Per-user notification preferences. No dedicated table exists yet in
this scaffold — defaults to all channels enabled. Add a
NotificationPreference model + migration before wiring real opt-outs."""

DEFAULT_PREFERENCES = {"email": True, "push": True, "in_app": True}


def get_preferences(user) -> dict:
    return DEFAULT_PREFERENCES.copy()
