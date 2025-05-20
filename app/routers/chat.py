from fastapi import APIRouter
from pydantic import BaseModel
router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatMessage(BaseModel):
    message: str

    @router.get("")
    async def get_chat(id: str):
        return {"message": "Hello, World!"}

    @router.get("/{id}")
    async def get_chat(id: str):
        return {"message": "Hello, World!"}
