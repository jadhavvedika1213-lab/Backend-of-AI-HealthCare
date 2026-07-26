from typing import List
from models.history import History
from repositories.history_repo import HistoryRepository
from schemas.history import HistoryCreate

class HistoryService:
    def __init__(self, db):
        self.repo = HistoryRepository(db)

    async def log_history_event(self, user_id: int, event_type: str, description: str, details: Optional[str] = None) -> History:
        history = History(
            user_id=user_id,
            event_type=event_type,
            description=description,
            details=details
        )
        return await self.repo.create(history)

    async def get_user_history(self, user_id: int, skip: int = 0, limit: int = 100) -> List[History]:
        return await self.repo.get_by_user_id(user_id, skip, limit)
