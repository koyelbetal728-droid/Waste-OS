"""Embedding interface. No embedding model is bundled here (would need a
real model download this environment can't perform) — packages/ai/rag
currently retrieves via keyword overlap (retriever.py), which is honest and
fully functional without external downloads. This module defines the
interface so a real sentence-transformer can be dropped in without
touching retriever.py's callers."""
from abc import ABC, abstractmethod


class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        ...


def get_embedder() -> BaseEmbedder | None:
    # No embedding backend configured — retriever.py falls back to keyword
    # matching rather than pretending vector search is active.
    return None
