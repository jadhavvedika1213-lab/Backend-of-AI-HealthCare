from core.database import clean_document, next_id
from models.report import Report


class ReportRepository:
    def __init__(self, db): self.db = db
    async def get_by_id(self, report_id): return Report.from_document(clean_document(await self.db.reports.find_one({"id": report_id})))
    async def get_by_user_id(self, user_id, skip=0, limit=100): return [Report.from_document(clean_document(d)) async for d in self.db.reports.find({"user_id": user_id}).sort("uploaded_at", -1).skip(skip).limit(limit)]
    async def create(self, report): report.id = await next_id("reports"); await self.db.reports.insert_one(report.to_document()); return report
    async def delete(self, report_id): return (await self.db.reports.delete_one({"id": report_id})).deleted_count == 1
    async def update(self, report): await self.db.reports.replace_one({"id": report.id}, report.to_document()); return report
