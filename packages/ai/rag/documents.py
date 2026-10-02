"""Document ingestion helpers for growing the RAG knowledge base beyond the
hard-coded seed list in knowledge_base.py."""
from packages.ai.rag.knowledge_base import DOCUMENTS


def add_document(doc_id: str, title: str, text: str, jurisdiction: str = "default") -> dict:
    entry = {"id": doc_id, "title": title, "text": text, "jurisdiction": jurisdiction}
    DOCUMENTS.append(entry)  # in-memory for this scaffold; persist to DB for production
    return entry
