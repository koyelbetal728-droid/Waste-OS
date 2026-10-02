"""Medical waste MUST follow authorized compliance workflow. AI may assist
classification, but never independently determines a disposal pathway here."""

RESTRICTED_CATEGORIES = {"sharps", "infectious", "pharmaceutical", "pathological"}


def requires_authorized_handling(category: str | None) -> bool:
    if not category:
        return True  # unknown -> conservative: require authorized review
    return category.lower() in RESTRICTED_CATEGORIES


def compliance_status(category: str | None) -> dict:
    restricted = requires_authorized_handling(category)
    return {
        "category": category or "unknown",
        "requires_authorized_facility": restricted,
        "recommended_action": "route_to_licensed_facility" if restricted else "standard_review",
    }
