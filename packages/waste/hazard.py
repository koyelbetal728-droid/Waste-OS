"""Hazard screening — conservative by design. Never confidently declares
something safe from insufficient visual evidence."""

HAZARD_KEYWORDS = {"battery", "chemical", "sharps", "medical", "pressurized", "e-waste"}


def screen_hazard(category: str | None, confidence: float | None) -> str:
    if not category:
        return "unknown"
    lowered = category.lower()
    if any(k in lowered for k in HAZARD_KEYWORDS):
        if confidence is not None and confidence >= 0.8:
            return "hazardous"
        return "potentially_hazardous"
    return "none_detected"
