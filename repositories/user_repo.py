from typing import Optional

from core.database import clean_document, next_id, utcnow
from models.user import User
from schemas.user import UserUpdate


class UserRepository:
    def __init__(self, db): self.db = db
    async def get_by_id(self, user_id: int) -> Optional[User]:
        return User.from_document(clean_document(await self.db.users.find_one({"id": user_id})))
    async def get_by_email(self, email: str) -> Optional[User]:
        return User.from_document(clean_document(await self.db.users.find_one({"email": email.lower()})))
    async def create(self, user: User) -> User:
        user.id = await next_id("users"); user.email = user.email.lower()
        await self.db.users.insert_one(user.to_document()); return user
    async def update(self, user_id: int, obj_in: UserUpdate) -> Optional[User]:
        values = obj_in.model_dump(exclude_unset=True)
        if "password" in values:
            from core.security import get_password_hash
            values["hashed_password"] = get_password_hash(values.pop("password"))
        if values:
            values["updated_at"] = utcnow()
            await self.db.users.update_one({"id": user_id}, {"$set": values})
        return await self.get_by_id(user_id)
    async def get_all(self, skip=0, limit=100):
        return [User.from_document(clean_document(d)) async for d in self.db.users.find({}).sort("created_at", -1).skip(skip).limit(limit)]
    async def set_active(self, user_id: int, active: bool) -> Optional[User]:
        await self.db.users.update_one({"id": user_id}, {"$set": {"is_active": active, "updated_at": utcnow()}})
        return await self.get_by_id(user_id)
