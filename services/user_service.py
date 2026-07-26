from typing import List, Optional
from models.user import User
from repositories.user_repo import UserRepository
from schemas.user import UserUpdate

class UserService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    async def get_profile(self, user_id: int) -> Optional[User]:
        return await self.repo.get_by_id(user_id)

    async def update_profile(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        return await self.repo.update(user_id, user_update)

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.repo.get_all(skip, limit)
        
    async def toggle_user_active(self, user_id: int) -> Optional[User]:
        user = await self.repo.get_by_id(user_id)
        if not user:
            return None
        return await self.repo.set_active(user_id, not user.is_active)
