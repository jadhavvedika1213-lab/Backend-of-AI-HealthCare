from models.base import Document, now


class Feedback(Document):
    @classmethod
    def defaults(cls):
        return {"category": "general", "comment": None, "created_at": now}
