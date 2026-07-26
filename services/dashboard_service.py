from typing import Dict, Any
from sqlalchemy import select
from models.report import Report
from models.prescription import Prescription
from models.reminder import Reminder
from models.notification import Notification

class DashboardService:
    def __init__(self, db):
        self.db = db

    async def get_dashboard_summary(self, user_id: int) -> Dict[str, Any]:
        """
        Aggregate recent documents, alerts, and counts for a user.
        """
        # Fetch 3 recent reports
        reports_res = await self.db.execute(
            select(Report)
            .filter(Report.user_id == user_id)
            .order_by(Report.uploaded_at.desc())
            .limit(3)
        )
        reports = reports_res.scalars().all()

        # Fetch 3 recent prescriptions
        presc_res = await self.db.execute(
            select(Prescription)
            .filter(Prescription.user_id == user_id)
            .order_by(Prescription.date.desc())
            .limit(3)
        )
        prescriptions = presc_res.scalars().all()

        # Fetch active reminders
        reminders_res = await self.db.execute(
            select(Reminder)
            .filter(Reminder.user_id == user_id, Reminder.is_active == True)
            .limit(5)
        )
        reminders = reminders_res.scalars().all()

        # Count unread notifications
        notifs_count_res = await self.db.execute(
            select(Notification)
            .filter(Notification.user_id == user_id, Notification.is_read == False)
        )
        unread_notifications_count = len(notifs_count_res.scalars().all())

        return {
            "stats": {
                "total_reports": len(reports),
                "total_prescriptions": len(prescriptions),
                "active_reminders_count": len(reminders),
                "unread_notifications": unread_notifications_count
            },
            "recent_reports": [
                {"id": r.id, "filename": r.filename, "uploaded_at": r.uploaded_at.isoformat(), "category": r.category}
                for r in reports
            ],
            "recent_prescriptions": [
                {"id": p.id, "doctor": p.doctor_name, "clinic": p.clinic_name, "date": p.date.isoformat()}
                for p in prescriptions
            ],
            "upcoming_reminders": [
                {"id": rem.id, "title": rem.title, "time": rem.time, "type": rem.reminder_type}
                for rem in reminders
            ]
        }
