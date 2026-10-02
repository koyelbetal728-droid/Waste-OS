"""Decides which AI component(s) a request needs. Not every request goes to
the LLM — a pure image scan never touches it, for example."""


def route(context) -> list[str]:
    needed = []
    if context.image_bytes:
        needed.append("vision")
    if context.user_question:
        needed.append("rag")
        needed.append("llm")
    return needed
