from models.base import Document, now


class AnalyticsEvent(Document):
    @classmethod
    def defaults(cls):
        return {"user_id": None, "metadata_json": None, "created_at": now}
