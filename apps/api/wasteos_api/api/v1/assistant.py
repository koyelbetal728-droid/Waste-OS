"""Generative-UI assistant endpoint. Classifies intent deterministically
(packages/ai/orchestrator/ui_intents.py), then resolves it against real,
live data (packages/ai/orchestrator/ui_resolver.py). The frontend renders
whatever component `type` comes back — this endpoint is what makes the UI
"generative": the backend decides the shape of the response per request."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.database.session import get_db
from packages.database.models.user import User
from packages.ai.orchestrator.ui_intents import classify_intent
from packages.ai.orchestrator.ui_resolver import resolve
from packages.observability.metrics import increment
from wasteos_api.schemas.assistant import AssistantQueryRequest, AssistantResponse
from wasteos_api.dependencies import get_current_user

router = APIRouter()


@router.post("/query", response_model=AssistantResponse)
def query_assistant(payload: AssistantQueryRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    intent = classify_intent(payload.message)
    increment(f"assistant_intent.{intent}")
    result = resolve(intent, db, user, payload.message)
    return AssistantResponse(intent=intent, **result)
