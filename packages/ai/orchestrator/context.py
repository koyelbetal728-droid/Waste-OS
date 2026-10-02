"""Request context passed through the orchestrator — keeps system
instructions, retrieved data, and user input clearly separated (retrieved
text is data, never instructions)."""
from dataclasses import dataclass, field


@dataclass
class AIContext:
    user_question: str | None = None
    image_bytes: bytes | None = None
    location: tuple[float, float] | None = None
    retrieved_documents: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
