from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.reminder_service import ReminderService
from core.database import get_db
from utils.response import APIResponse
from schemas.reminder import ReminderCreate, ReminderUpdate, ReminderResponse
from typing import List

router = APIRouter()

@router.post("", response_model=ReminderResponse)
async def create_reminder(
    reminder_in: ReminderCreate,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = ReminderService(db)
    reminder = await service.add_reminder(current_user.id, reminder_in)
    return reminder

@router.get("", response_model=List[ReminderResponse])
async def list_reminders(
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = ReminderService(db)
    items = await service.list_reminders(current_user.id)
    return items

@router.put("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(
    reminder_id: int,
    update_in: ReminderUpdate,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = ReminderService(db)
    updated = await service.update_reminder(current_user.id, reminder_id, update_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Reminder not found or permission denied.")
    return updated

@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = ReminderService(db)
    success = await service.delete_reminder(current_user.id, reminder_id)
    if success:
        return APIResponse.success(message="Reminder deleted successfully.")
    raise HTTPException(status_code=404, detail="Reminder not found.")
