from fastapi import APIRouter, Depends, Query
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.search_service import SearchService
from core.database import get_db
from utils.response import APIResponse

router = APIRouter()

@router.get("")
async def search_records(
    q: str = Query(..., min_length=1, description="Search keyword"),
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = SearchService(db)
    results = await service.search_user_records(current_user.id, q)
    return APIResponse.success(
        message="Search completed successfully.",
        data=results
    )
