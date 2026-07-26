from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from dependencies.role_dependency import RoleChecker
from services.user_service import UserService
from services.analytics_service import AnalyticsService
from core.database import get_db
from core.constants import UserRole
from utils.response import APIResponse
from schemas.user import UserResponse
from typing import List

router = APIRouter()

# Instantiate checker for Admin role only
admin_only = RoleChecker([UserRole.ADMIN])

@router.get("/users", response_model=List[UserResponse])
async def admin_list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(admin_only),
    db = Depends(get_db)
):
    service = UserService(db)
    users = await service.list_users(skip, limit)
    return users

@router.post("/users/{user_id}/toggle-active")
async def admin_toggle_user(
    user_id: int,
    current_user: User = Depends(admin_only),
    db = Depends(get_db)
):
    service = UserService(db)
    user = await service.toggle_user_active(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
        
    state = "activated" if user.is_active else "deactivated"
    return APIResponse.success(message=f"User has been successfully {state}.")

@router.get("/system-health")
async def get_system_health(
    current_user: User = Depends(admin_only),
    db = Depends(get_db)
):
    """
    Overview telemetry metrics for admins.
    """
    analytics = AnalyticsService(db)
    metrics = await analytics.get_metrics()
    return APIResponse.success(
        message="System telemetry retrieved.",
        data={
            "metrics": metrics,
            "api_version": "1.0.0",
            "environment": "development"
        }
    )
