from core.database import clean_document, next_id, utcnow
from models.reminder import Reminder


class ReminderRepository:
    def __init__(self, db): self.db = db
    async def get_by_id(self, reminder_id): return Reminder.from_document(clean_document(await self.db.reminders.find_one({"id": reminder_id})))
    async def get_by_user_id(self, user_id): return [Reminder.from_document(clean_document(d)) async for d in self.db.reminders.find({"user_id": user_id}).sort("created_at", -1)]
    async def create(self, reminder): reminder.id = await next_id("reminders"); await self.db.reminders.insert_one(reminder.to_document()); return reminder
    async def update(self, reminder_id, obj_in):
        values = obj_in.model_dump(exclude_unset=True); values["updated_at"] = utcnow()
        await self.db.reminders.update_one({"id": reminder_id}, {"$set": values}); return await self.get_by_id(reminder_id)
    async def delete(self, reminder_id): return (await self.db.reminders.delete_one({"id": reminder_id})).deleted_count == 1
    async def get_active_reminders(self): return [Reminder.from_document(clean_document(d)) async for d in self.db.reminders.find({"is_active": True})]
