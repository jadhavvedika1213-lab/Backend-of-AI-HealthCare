from core.database import clean_document, next_id
from models.analytics import AnalyticsEvent

class AnalyticsRepository:
    def __init__(self, db): self.db = db
    async def log_event(self, event): event.id = await next_id("analytics_events"); await self.db.analytics_events.insert_one(event.to_document()); return event
    async def get_all_events(self, skip=0, limit=200): return [AnalyticsEvent.from_document(clean_document(d)) async for d in self.db.analytics_events.find({}).sort("created_at", -1).skip(skip).limit(limit)]
    async def get_events_by_name(self, event_name): return [AnalyticsEvent.from_document(clean_document(d)) async for d in self.db.analytics_events.find({"event_name": event_name}).sort("created_at", -1)]
