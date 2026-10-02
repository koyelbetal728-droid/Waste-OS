"""Centralized cache key builders so callers never hand-format a key
string (and risk a typo causing a cache-poisoning bug)."""


def waste_taxonomy_key() -> str:
    return "cache:waste_taxonomy"


def facility_list_key(facility_type: str | None) -> str:
    return f"cache:facilities:{facility_type or 'all'}"


def dashboard_analytics_key(org_id: str | None) -> str:
    return f"cache:analytics:{org_id or 'platform'}"
