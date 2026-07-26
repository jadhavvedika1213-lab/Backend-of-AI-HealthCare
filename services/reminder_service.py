from datetime import datetime, timezone
from typing import List, Optional
from models.reminder import Reminder
from repositories.reminder_repo import ReminderRepository
from schemas.reminder import ReminderCreate, ReminderUpdate
from core.constants import ReminderStatus
from core.logger import logger

class ReminderService:
    def __init__(self, db):
        self.repo = ReminderRepository(db)

    async def add_reminder(self, user_id: int, reminder_in: ReminderCreate) -> Reminder:
        reminder = Reminder(
            user_id=user_id,
            title=reminder_in.title,
            reminder_type=reminder_in.reminder_type,
            time=reminder_in.time,
            frequency=reminder_in.frequency,
            is_active=reminder_in.is_active,
            email_notification=reminder_in.email_notification,
            status=ReminderStatus.PENDING
        )
        return await self.repo.create(reminder)

    async def list_reminders(self, user_id: int) -> List[Reminder]:
        return await self.repo.get_by_user_id(user_id)

    async def update_reminder(self, user_id: int, reminder_id: int, update_in: ReminderUpdate) -> Optional[Reminder]:
        reminder = await self.repo.get_by_id(reminder_id)
        if not reminder or reminder.user_id != user_id:
            return None
        return await self.repo.update(reminder_id, update_in)

    async def delete_reminder(self, user_id: int, reminder_id: int) -> bool:
        reminder = await self.repo.get_by_id(reminder_id)
        if not reminder or reminder.user_id != user_id:
            return False
        return await self.repo.delete(reminder_id)

    async def trigger_pending_reminders(self) -> None:
        """
        Runs as background cron to dispatch due notifications.
        Since SQLite is simple, we compare current hour/minute with reminder.time.
        """
        active_reminders = await self.repo.get_active_reminders()
        current_time_str = datetime.now().strftime("%H:%M")  # e.g., "08:30"
        
        for reminder in active_reminders:
            # Simple string matching for HH:MM format
            if reminder.time == current_time_str:
                logger.info(f"Triggering reminder: {reminder.title} for user {reminder.user_id}")
                
                # Update last triggered
                reminder.last_triggered = datetime.now(timezone.utc)
                await self.repo.db.reminders.update_one({"id": reminder.id}, {"$set": {"last_triggered": reminder.last_triggered}})
                
                # Send Email if enabled
                if reminder.email_notification:
                    try:
                        from models.user import User
                        from core.database import clean_document
                        user = User.from_document(clean_document(await self.repo.db.users.find_one({"id": reminder.user_id})))
                        if user:
                            from services.email_service import EmailService
                            await EmailService.send_reminder_email(
                                email=user.email,
                                name=user.full_name,
                                reminder_title=reminder.title,
                                reminder_time=reminder.time
                            )
                    except Exception as e:
                        logger.error(f"Failed to send reminder email: {str(e)}")
                        
                # Create System Notification
                try:
                    from models.notification import Notification
                    notif = Notification(
                        user_id=reminder.user_id,
                        title=f"Time for your {reminder.reminder_type}",
                        message=reminder.title,
                        notification_type="reminder"
                    )
                    from core.database import next_id
                    notif.id = await next_id("notifications")
                    await self.repo.db.notifications.insert_one(notif.to_document())
                except Exception as e:
                    logger.error(f"Failed to record reminder notification: {str(e)}")
                    
