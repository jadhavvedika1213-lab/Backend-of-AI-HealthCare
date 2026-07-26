from core.database import clean_document, next_id
from models.chat import ChatMessage, ChatSession


class ChatRepository:
    def __init__(self, db): self.db = db
    async def get_session(self, session_id): return ChatSession.from_document(clean_document(await self.db.chat_sessions.find_one({"id": session_id})))
    async def get_sessions_by_user_id(self, user_id): return [ChatSession.from_document(clean_document(d)) async for d in self.db.chat_sessions.find({"user_id": user_id}).sort("created_at", -1)]
    async def create_session(self, session): await self.db.chat_sessions.insert_one(session.to_document()); return session
    async def add_message(self, message): message.id = await next_id("chat_messages"); await self.db.chat_messages.insert_one(message.to_document()); return message
    async def get_messages(self, session_id): return [ChatMessage.from_document(clean_document(d)) async for d in self.db.chat_messages.find({"session_id": session_id}).sort("created_at", 1)]
    async def delete_session(self, session_id):
        result = await self.db.chat_sessions.delete_one({"id": session_id}); await self.db.chat_messages.delete_many({"session_id": session_id}); return result.deleted_count == 1
