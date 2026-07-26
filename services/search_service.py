from typing import List, Dict, Any
from models.report import Report
from models.prescription import Prescription
from models.reminder import Reminder

class SearchService:
    def __init__(self, db):
        self.db = db

    async def search_user_records(self, user_id: int, query: str) -> Dict[str, List[Any]]:
        """
        Global keyword search across Reports, Prescriptions, and Reminders for the user.
        """
        query_pattern = f"%{query}%"

        # Search Reports
        reports_query = select(Report).filter(
            Report.user_id == user_id,
            (Report.filename.like(query_pattern)) | 
            (Report.category.like(query_pattern)) |
            (Report.ocr_content.like(query_pattern)) |
            (Report.summary.like(query_pattern))
        )
        reports_res = await self.db.execute(reports_query)
        reports = reports_res.scalars().all()

        # Search Prescriptions
        prescriptions_query = select(Prescription).filter(
            Prescription.user_id == user_id,
            (Prescription.doctor_name.like(query_pattern)) |
            (Prescription.clinic_name.like(query_pattern)) |
            (Prescription.raw_text.like(query_pattern)) |
            (Prescription.summary.like(query_pattern))
        )
        prescriptions_res = await self.db.execute(prescriptions_query)
        prescriptions = prescriptions_res.scalars().all()

        # Search Reminders
        reminders_query = select(Reminder).filter(
            Reminder.user_id == user_id,
            (Reminder.title.like(query_pattern)) |
            (Reminder.reminder_type.like(query_pattern))
        )
        reminders_res = await self.db.execute(reminders_query)
        reminders = reminders_res.scalars().all()

        # Format results
        return {
            "reports": [
                {"id": r.id, "filename": r.filename, "category": r.category, "summary": r.summary}
                for r in reports
            ],
            "prescriptions": [
                {"id": p.id, "doctor": p.doctor_name, "clinic": p.clinic_name, "summary": p.summary}
                for p in prescriptions
            ],
            "reminders": [
                {"id": rem.id, "title": rem.title, "type": rem.reminder_type, "time": rem.time}
                for rem in reminders
            ]
        }
class GlobalSearchService(SearchService):
    pass
