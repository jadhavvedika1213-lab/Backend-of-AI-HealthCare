from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.chatbot_service import ChatbotService
from core.database import get_db
from utils.response import APIResponse
from schemas.chatbot import AskAIRequest, ChatSessionResponse, ChatMessageResponse
from typing import List
from core.logger import logger

router = APIRouter()

@router.post("/message")
async def send_message(
    payload: AskAIRequest,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    try:
        service = ChatbotService(db)
        session = await service.get_or_create_session(current_user.id, payload.session_id)
        assistant_msg = await service.send_chatbot_message(current_user.id, session.id, payload.prompt)

        return APIResponse.success(
            message="Message dispatched successfully.",
            data={
                "session_id": session.id,
                "user_prompt": payload.prompt,
                "assistant_reply": assistant_msg.content,
                "created_at": assistant_msg.created_at.isoformat()
            }
        )
    except Exception:
        # Keep the companion usable if persistence or an optional AI provider is
        # temporarily unavailable. The exception remains available in Render logs.
        logger.exception("Chatbot message processing failed")
        return APIResponse.success(
            message="Chatbot is temporarily running in fallback mode.",
            data={
                "session_id": payload.session_id,
                "user_prompt": payload.prompt,
                "assistant_reply": "I received your message. The AI service is temporarily unavailable, so please try again shortly. For urgent symptoms, contact a qualified medical professional.",
                "created_at": None,
            },
        )

@router.get("/sessions", response_model=List[ChatSessionResponse])
async def list_sessions(
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = ChatbotService(db)
    sessions = await service.list_sessions(current_user.id)
    return sessions

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_messages(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = ChatbotService(db)
    messages = await service.get_messages(session_id, current_user.id)
    return messages

@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = ChatbotService(db)
    success = await service.delete_session(session_id, current_user.id)
    if success:
        return APIResponse.success(message="Chat session deleted successfully.")
    raise HTTPException(status_code=404, detail="Chat session not found.")
