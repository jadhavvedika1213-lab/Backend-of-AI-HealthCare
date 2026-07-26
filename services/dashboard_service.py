import asyncio
from typing import Dict, Any

class DashboardService:
    def __init__(self, db):
        self.db = db

    async def get_dashboard_summary(self, user_id: int) -> Dict[str, Any]:
        """
        Aggregate recent documents, alerts, and counts for a user.
        """
        # The application uses Motor/MongoDB, not SQLAlchemy.
        reports = [
            report async for report in self.db.reports.find({"user_id": user_id})
            .sort("uploaded_at", -1).limit(3)
        ]
        prescriptions = [
            prescription async for prescription in self.db.prescriptions.find({"user_id": user_id})
            .sort("date", -1).limit(3)
        ]
        reminders = [
            reminder async for reminder in self.db.reminders.find({"user_id": user_id, "is_active": True})
            .sort("created_at", -1).limit(5)
        ]
        total_reports, total_prescriptions, active_reminders_count, unread_notifications_count = await asyncio.gather(
            self.db.reports.count_documents({"user_id": user_id}),
            self.db.prescriptions.count_documents({"user_id": user_id}),
            self.db.reminders.count_documents({"user_id": user_id, "is_active": True}),
            self.db.notifications.count_documents({"user_id": user_id, "is_read": False}),
        )

        return {
            "stats": {
                "total_reports": total_reports,
                "total_prescriptions": total_prescriptions,
                "active_reminders_count": active_reminders_count,
                "unread_notifications": unread_notifications_count
            },
            "recent_reports": [
                {"id": r["id"], "filename": r["filename"], "uploaded_at": r["uploaded_at"].isoformat(), "category": r["category"]}
                for r in reports
            ],
            "recent_prescriptions": [
                {"id": p["id"], "doctor": p.get("doctor_name"), "clinic": p.get("clinic_name"), "date": p["date"].isoformat()}
                for p in prescriptions
            ],
            "upcoming_reminders": [
                {"id": rem["id"], "title": rem["title"], "time": rem["time"], "type": rem["reminder_type"]}
                for rem in reminders
            ]
        }
