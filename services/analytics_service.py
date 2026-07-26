import json
from models.analytics import AnalyticsEvent
from repositories.analytics_repo import AnalyticsRepository
from schemas.analytics import AnalyticsEventCreate
from typing import List, Dict, Any, Optional

class AnalyticsService:
    def __init__(self, db):
        self.repo = AnalyticsRepository(db)

    async def record_event(self, event_name: str, user_id: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None) -> AnalyticsEvent:
        metadata_str = json.dumps(metadata) if metadata else None
        event = AnalyticsEvent(
            event_name=event_name,
            user_id=user_id,
            metadata_json=metadata_str
        )
        return await self.repo.log_event(event)

    async def get_metrics(self) -> Dict[str, Any]:
        """
        Produce a summary of events for admin visualization.
        """
        events = await self.repo.get_all_events(limit=500)
        total_events = len(events)
        
        # Simple frequency counts
        event_counts = {}
        user_activity = set()
        
        for e in events:
            event_counts[e.event_name] = event_counts.get(e.event_name, 0) + 1
            if e.user_id:
                user_activity.add(e.user_id)
                
        return {
            "total_logged_events": total_events,
            "unique_active_users_counted": len(user_activity),
            "event_frequency_breakdown": event_counts
        }
