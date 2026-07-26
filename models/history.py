from models.base import Document, now


class History(Document):
    @classmethod
    def defaults(cls):
        return {"details": None, "recorded_at": now}
