from fastapi import APIRouter, Depends
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.dashboard_service import DashboardService
from core.database import get_db
from utils.response import APIResponse

router = APIRouter()

@router.get("")
async def get_dashboard(
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = DashboardService(db)
    summary = await service.get_dashboard_summary(current_user.id)
    return APIResponse.success(
        message="Fetched dashboard summary successfully.",
        data=summary
    )
