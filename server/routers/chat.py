from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

from services.chat_service import chat_service
from dependencies import get_current_user
import models

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    language: str = "en"

class ChatResponse(BaseModel):
    reply: str
    language: str

@router.post("/message", response_model=ChatResponse)
async def chat_message(
    request: ChatRequest,
    current_user: models.User = Depends(get_current_user)
):
    # 1. Get Response from AI
    reply = await chat_service.get_response(request.message, language=request.language)
    
    # 2. Save User Message
    user_msg = models.ChatHistory(
        user_id=current_user.id,
        role="user",
        message=request.message
    )
    await user_msg.insert()
    
    # 3. Save Bot Response
    bot_msg = models.ChatHistory(
        user_id=current_user.id,
        role="bot",
        message=reply
    )
    await bot_msg.insert()
    
    return {
        "reply": reply,
        "language": request.language
    }

@router.get("/history")
async def get_chat_history(
    current_user: models.User = Depends(get_current_user)
):
    history = await models.ChatHistory.find(
        models.ChatHistory.user_id == current_user.id
    ).sort(+models.ChatHistory.created_at).to_list()
    
    return history
