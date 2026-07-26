from core.constants import UserRole
from models.base import Document, now


class User(Document):
    @classmethod
    def defaults(cls):
        return {"role": UserRole.PATIENT, "is_active": True, "full_name": None,
                "phone_number": None, "created_at": now, "updated_at": now}
