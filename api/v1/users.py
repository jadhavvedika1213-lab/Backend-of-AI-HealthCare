from fastapi import APIRouter, Depends
from typing import List
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from dependencies.common import CommonPagination, get_pagination_params
from schemas.user import UserResponse
from services.user_service import UserService
from core.database import get_db

router = APIRouter()

@router.get("", response_model=List[UserResponse])
async def list_users(
    pagination: CommonPagination = Depends(get_pagination_params),
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = UserService(db)
    users = await service.list_users(skip=pagination.skip, limit=pagination.limit)
    return users
