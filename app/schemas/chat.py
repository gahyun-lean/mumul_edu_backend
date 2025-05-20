from pydantic import BaseModel
class ChatRequest(BaseModel):
    question: str
    context_docs: list[str] = []

class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []
