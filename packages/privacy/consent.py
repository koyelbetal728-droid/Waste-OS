"""Minimal consent flag storage. Extend with a real ConsentLog table if you
need per-purpose consent tracking (marketing, analytics, etc.) — this
scaffold only tracks the single "processed" flag most flows need."""


def has_consented(user) -> bool:
    # Registration is the consent action in this scaffold's flow.
    return user.is_active
