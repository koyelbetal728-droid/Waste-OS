from pydantic import BaseModel


class AdvisoryRequest(BaseModel):
    question: str


class AdvisoryResponse(BaseModel):
    answer: str
    source: str
    retrieved_documents: list[str]
    warnings: list[str] = []
