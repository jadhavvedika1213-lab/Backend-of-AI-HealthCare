from typing import List, Optional
from models.report import Report
from repositories.report_repo import ReportRepository

class ReportService:
    def __init__(self, db):
        self.repo = ReportRepository(db)

    async def get_report(self, report_id: int, user_id: int) -> Optional[Report]:
        report = await self.repo.get_by_id(report_id)
        if report and report.user_id == user_id:
            return report
        return None

    async def list_reports(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Report]:
        return await self.repo.get_by_user_id(user_id, skip, limit)

    async def create_report_record(self, user_id: int, filename: str, file_path: str, category: str) -> Report:
        report = Report(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            category=category
        )
        return await self.repo.create(report)

    async def delete_report(self, report_id: int, user_id: int) -> bool:
        report = await self.get_report(report_id, user_id)
        if not report:
            return False
        return await self.repo.delete(report_id)
