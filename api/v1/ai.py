from fastapi import APIRouter, Depends
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.ai_service import AIService
from utils.response import APIResponse
from pydantic import BaseModel

router = APIRouter()

class AIQueryRequest(BaseModel):
    prompt: str

@router.post("/query")
async def query_ai(
    request: AIQueryRequest,
    current_user: User = Depends(get_current_active_user)
):
    answer = await AIService.ask_general_question(request.prompt)
    return APIResponse.success(
        message="AI generated response successfully.",
        data={"answer": answer}
    )
