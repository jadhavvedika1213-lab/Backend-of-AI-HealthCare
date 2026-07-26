from models.base import Document, now


class Notification(Document):
    @classmethod
    def defaults(cls):
        return {"notification_type": "general", "is_read": False, "created_at": now}
