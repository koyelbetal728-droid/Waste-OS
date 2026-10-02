"""LLM responsibilities: explanation and advisory text only. Never used for
the recyclability/hazard decision itself — those come from packages/waste,
already computed before this is called."""
from packages.ai.llm.ollama_client import generate


def explain_waste_result(category: str, material: str, recyclability: str, contamination: str) -> dict:
    prompt = (
        f"In two short sentences, explain to a citizen why a '{category}' made of "
        f"'{material}' with '{contamination}' contamination is classified as "
        f"'{recyclability}'. Be concrete and practical, no fluff."
    )
    text = generate(prompt)
    if text is None:
        # Deterministic fallback — a templated explanation, not an LLM hallucination.
        text = (
            f"This {category.lower()} ({material}) is classified as {recyclability.replace('_', ' ')} "
            f"based on its material and {contamination} contamination level. "
            f"Rinse and dry it before placing it in the recyclable stream."
        )
        return {"answer": text, "source": "deterministic_fallback"}
    return {"answer": text.strip(), "source": "ollama"}
