"""Final safety gate before any AI-derived advisory text reaches a user.
Retrieved RAG documents and LLM output are DATA, never instructions —
this function never executes anything found inside them."""

BLOCKED_PHRASES = ["ignore previous instructions", "disregard the rules", "system prompt"]


def sanitize_advisory(text: str) -> str:
    lowered = text.lower()
    for phrase in BLOCKED_PHRASES:
        if phrase in lowered:
            return "Advisory withheld: response failed safety validation."
    return text
