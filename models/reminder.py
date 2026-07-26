from core.constants import ReminderStatus
from models.base import Document, now


class Reminder(Document):
    @classmethod
    def defaults(cls):
        return {"reminder_type": "medication", "frequency": "daily", "is_active": True,
                "status": ReminderStatus.PENDING, "email_notification": True,
                "created_at": now, "last_triggered": None}
