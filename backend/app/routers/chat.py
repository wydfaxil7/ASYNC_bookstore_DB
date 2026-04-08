# backend/app/routers/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.schemas import ChatRequest, ChatResponse
from app.services.chatbot import build_chat_turn

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat_endpoint(
    payload: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle one authenticated chatbot request with DB-aware context
    """
    return await build_chat_turn(db, current_user, payload)