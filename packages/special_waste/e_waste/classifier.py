"""E-waste pathway decision — deterministic rules layered on top of whatever
condition signal is available (AI or manual input). Final pathway always
respects configured policy; AI never independently decides disposal."""

CONDITION_TO_PATHWAY = {
    "working": "reuse",
    "minor_fault": "repair",
    "major_fault": "refurbish",
    "non_functional": "recycle",
}


def determine_pathway(condition: str | None) -> str:
    return CONDITION_TO_PATHWAY.get(condition, "recycle")  # conservative default
