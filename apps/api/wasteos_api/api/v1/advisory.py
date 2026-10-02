from fastapi import APIRouter, Depends
from packages.ai.rag.retriever import retrieve
from packages.ai.llm.ollama_client import generate
from packages.ai.orchestrator.safety import sanitize_advisory
from wasteos_api.schemas.advisory import AdvisoryRequest, AdvisoryResponse
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.post("", response_model=AdvisoryResponse)
def ask_advisory(payload: AdvisoryRequest, user=Depends(get_current_user)):
    """RAG + LLM advisory. Retrieved documents are treated as context data,
    never as instructions. Falls back to a deterministic answer if the LLM
    is unavailable — never fabricates a response either way."""
    docs = retrieve(payload.question)
    context = "\n".join(f"- {d['title']}: {d['text']}" for d in docs)
    prompt = (
        f"Answer the citizen's waste-management question using ONLY the context below. "
        f"If the context doesn't cover it, say so plainly.\n\nContext:\n{context}\n\n"
        f"Question: {payload.question}"
    )
    llm_answer = generate(prompt)
    if llm_answer is None:
        if docs:
            answer = docs[0]["text"]
            source = "rag_fallback"
        else:
            answer = "I don't have guidance on that yet — please check your local municipal rules."
            source = "no_match"
    else:
        answer = llm_answer.strip()
        source = "ollama_rag"

    return AdvisoryResponse(
        answer=sanitize_advisory(answer),
        source=source,
        retrieved_documents=[d["title"] for d in docs],
    )
