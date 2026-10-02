"""Text-modality entry point — routes free-text questions to RAG+LLM."""
from packages.ai.rag.retriever import retrieve
from packages.ai.llm.ollama_client import generate


def process_text(question: str) -> dict:
    docs = retrieve(question)
    context = "\n".join(f"- {d['text']}" for d in docs)
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer using only the context."
    answer = generate(prompt)
    if answer is None:
        answer = docs[0]["text"] if docs else "No guidance available for that question yet."
    return {"answer": answer, "sources": [d["title"] for d in docs]}
