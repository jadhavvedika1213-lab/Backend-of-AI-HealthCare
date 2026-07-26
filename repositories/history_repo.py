from core.database import clean_document, next_id
from models.history import History

class HistoryRepository:
    def __init__(self, db): self.db = db
    async def create(self, history): history.id = await next_id("histories"); await self.db.histories.insert_one(history.to_document()); return history
    async def get_by_user_id(self, user_id, skip=0, limit=100): return [History.from_document(clean_document(d)) async for d in self.db.histories.find({"user_id": user_id}).sort("recorded_at", -1).skip(skip).limit(limit)]
