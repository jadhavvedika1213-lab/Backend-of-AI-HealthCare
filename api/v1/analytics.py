from fastapi import APIRouter, Depends
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from dependencies.role_dependency import RoleChecker
from services.analytics_service import AnalyticsService
from core.database import get_db
from core.constants import UserRole
from utils.response import APIResponse
from schemas.analytics import AnalyticsEventCreate

router = APIRouter()

@router.post("/log")
async def log_telemetry_event(
    event: AnalyticsEventCreate,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = AnalyticsService(db)
    # Parse metadata json if valid
    import json
    metadata = None
    if event.metadata_json:
        try:
            metadata = json.loads(event.metadata_json)
        except json.JSONDecodeError:
            pass
            
    await service.record_event(event.event_name, current_user.id, metadata)
    return APIResponse.success(message="Analytics telemetry logged.")

@router.get("/summary")
async def get_analytics_summary(
    current_user: User = Depends(RoleChecker([UserRole.ADMIN])),
    db = Depends(get_db)
):
    """
    Admin only telemetry overview.
    """
    service = AnalyticsService(db)
    metrics = await service.get_metrics()
    return APIResponse.success(
        message="Fetched system telemetry metrics.",
        data=metrics
    )
