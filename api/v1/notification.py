from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.notification_service import NotificationService
from core.database import get_db
from utils.response import APIResponse

router = APIRouter()

@router.get("")
async def list_notifications(
    unread_only: bool = False,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = NotificationService(db)
    items = await service.get_user_notifications(current_user.id, unread_only=unread_only)
    
    # Simple serialize since notification list is short
    data = [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "notification_type": n.notification_type,
            "is_read": n.is_read,
            "created_at": n.created_at.isoformat()
        }
        for n in items
    ]
    return APIResponse.success(message="Notifications fetched successfully.", data=data)

@router.put("/{notification_id}/read")
async def mark_read(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = NotificationService(db)
    notif = await service.mark_as_read(notification_id, current_user.id)
    if notif:
        return APIResponse.success(message="Notification marked as read.")
    raise HTTPException(status_code=404, detail="Notification not found.")

@router.put("/read-all")
async def mark_all_read(
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = NotificationService(db)
    count = await service.mark_all_read(current_user.id)
    return APIResponse.success(message=f"Marked {count} notifications as read.")

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = NotificationService(db)
    success = await service.delete_notification(notification_id, current_user.id)
    if success:
        return APIResponse.success(message="Notification deleted successfully.")
    raise HTTPException(status_code=404, detail="Notification not found.")
