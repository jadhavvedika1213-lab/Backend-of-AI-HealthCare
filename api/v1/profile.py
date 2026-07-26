from fastapi import APIRouter, Depends
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from schemas.user import UserUpdate, UserResponse
from services.user_service import UserService
from core.database import get_db
from utils.response import APIResponse

router = APIRouter()

@router.get("", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = UserService(db)
    updated_user = await service.update_profile(current_user.id, user_update)
    return updated_user
