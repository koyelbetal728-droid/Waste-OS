"""Deterministic intent classifier for the generative-UI assistant.
Keyword-based on purpose: real, auditable routing — never an LLM guessing
which UI to render. Each intent maps to a real data-fetching function and
a UI component type the frontend knows how to render.

This is intentionally NOT an LLM call: which component renders is a
structural decision that must be reliable, not probabilistic. The LLM
(packages/ai/llm) is still used separately for free-text explanation
inside a "text" response when nothing more specific matches.
"""
import re

INTENT_PATTERNS = [
    ("waste_stats", [r"\bwaste\b.*\b(stat|summary|total)\b", r"\bhow much\b.*\bwaste\b", r"\bmy waste\b"]),
    ("recycling_rate", [r"\brecycl(e|ing) rate\b", r"\bhow much.*recycl", r"\bdiversion\b"]),
    ("schedule_pickup", [r"\bschedule\b.*\bpickup\b", r"\bpickup\b.*\brequest\b", r"\bbook.*pickup\b", r"\bneed.*pickup\b"]),
    ("forecast", [r"\bforecast\b", r"\bpredict\b.*waste", r"\bnext week\b.*waste"]),
    ("hotspots", [r"\bhotspots?\b", r"\bdumping\b", r"\bwhere.*(problem|illegal)\b"]),
    ("rewards", [r"\bgreen points\b", r"\breward\b", r"\bpoints\b"]),
    ("marketplace", [r"\blisting\b", r"\bmarketplace\b", r"\bsell.*material\b", r"\bbuy.*material\b"]),
    ("recyclability_check", [r"\bcan i recycle\b", r"\bis.*recyclable\b", r"\brecycle this\b"]),
]


def classify_intent(message: str) -> str:
    lowered = message.lower()
    for intent, patterns in INTENT_PATTERNS:
        if any(re.search(p, lowered) for p in patterns):
            return intent
    return "unknown"
