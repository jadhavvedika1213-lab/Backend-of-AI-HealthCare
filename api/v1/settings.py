from fastapi import APIRouter, Depends
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from utils.response import APIResponse
from pydantic import BaseModel

router = APIRouter()

class UserSettingsUpdate(BaseModel):
    receive_emails: bool
    theme: str = "dark"

@router.get("")
async def get_settings(current_user: User = Depends(get_current_active_user)):
    # Standard settings object
    return APIResponse.success(
        message="Fetched application settings.",
        data={
            "receive_emails": True,
            "theme": "dark",
            "mfa_enabled": False,
            "role": current_user.role
        }
    )

@router.put("")
async def update_settings(
    settings_in: UserSettingsUpdate,
    current_user: User = Depends(get_current_active_user)
):
    return APIResponse.success(
        message="Settings updated successfully.",
        data={
            "receive_emails": settings_in.receive_emails,
            "theme": settings_in.theme
        }
    )
