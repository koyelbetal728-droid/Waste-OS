from pydantic import BaseModel
from typing import Any


class AssistantQueryRequest(BaseModel):
    message: str


class AssistantResponse(BaseModel):
    type: str
    title: str
    data: dict[str, Any]
    intent: str
