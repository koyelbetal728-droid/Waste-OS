from packages.ai.rag.knowledge_base import DOCUMENTS


def retrieve(query: str, top_k: int = 2) -> list[dict]:
    """Naive keyword overlap scoring. Retrieved documents are treated as
    data for the LLM, never as instructions (see packages/ai/orchestrator/safety.py)."""
    query_terms = set(query.lower().split())
    scored = []
    for doc in DOCUMENTS:
        doc_terms = set((doc["title"] + " " + doc["text"]).lower().split())
        overlap = len(query_terms & doc_terms)
        if overlap:
            scored.append((overlap, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]
