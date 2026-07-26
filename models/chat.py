from models.base import Document, now


class ChatSession(Document):
    @classmethod
    def defaults(cls):
        return {"title": "New Conversation", "created_at": now, "messages": list}


class ChatMessage(Document):
    @classmethod
    def defaults(cls):
        return {"created_at": now}
