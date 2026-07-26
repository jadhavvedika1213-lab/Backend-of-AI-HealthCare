from typing import List, Optional
from models.notification import Notification

class NotificationService:
    def __init__(self, db):
        self.db = db

    async def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[Notification]:
        query = select(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        query = query.order_by(Notification.created_at.desc())
        
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def mark_as_read(self, notification_id: int, user_id: int) -> Optional[Notification]:
        result = await self.db.execute(
            select(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id)
        )
        notif = result.scalars().first()
        if notif:
            notif.is_read = True
            await self.db.commit()
            await self.db.refresh(notif)
        return notif

    async def mark_all_read(self, user_id: int) -> int:
        result = await self.db.execute(
            select(Notification).filter(Notification.user_id == user_id, Notification.is_read == False)
        )
        notifs = result.scalars().all()
        count = 0
        for notif in notifs:
            notif.is_read = True
            count += 1
        if count > 0:
            await self.db.commit()
        return count

    async def create_notification(self, user_id: int, title: str, message: str, notification_type: str = "general") -> Notification:
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type
        )
        self.db.add(notif)
        await self.db.commit()
        await self.db.refresh(notif)
        return notif
        
    async def delete_notification(self, notification_id: int, user_id: int) -> bool:
        result = await self.db.execute(
            select(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id)
        )
        notif = result.scalars().first()
        if not notif:
            return False
        await self.db.delete(notif)
        await self.db.commit()
        return True
