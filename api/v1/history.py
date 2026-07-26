from fastapi import APIRouter, Depends
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from dependencies.common import CommonPagination, get_pagination_params
from services.history_service import HistoryService
from core.database import get_db
from utils.response import APIResponse
from schemas.history import HistoryResponse, HistoryCreate
from typing import List

router = APIRouter()

@router.post("", response_model=HistoryResponse)
async def log_event(
    event: HistoryCreate,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = HistoryService(db)
    record = await service.log_history_event(
        user_id=current_user.id,
        event_type=event.event_type,
        description=event.description,
        details=event.details
    )
    return record

@router.get("", response_model=List[HistoryResponse])
async def get_history(
    pagination: CommonPagination = Depends(get_pagination_params),
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = HistoryService(db)
    records = await service.get_user_history(current_user.id, skip=pagination.skip, limit=pagination.limit)
    return records
