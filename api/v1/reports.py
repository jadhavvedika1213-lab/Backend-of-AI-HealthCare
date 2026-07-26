from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from dependencies.common import CommonPagination, get_pagination_params
from services.upload_service import UploadService
from services.report_service import ReportService
from core.database import get_db
from core.config import settings
from utils.response import APIResponse
from schemas.report import ReportResponse
from typing import List

router = APIRouter()

@router.post("/upload", response_model=ReportResponse)
async def upload_medical_report(
    category: str = "lab_report",
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    path = await UploadService.save_uploaded_file(file, settings.REPORTS_DIR)
    
    service = ReportService(db)
    report = await service.create_report_record(
        user_id=current_user.id,
        filename=file.filename,
        file_path=path,
        category=category
    )
    return report

@router.get("", response_model=List[ReportResponse])
async def list_reports(
    pagination: CommonPagination = Depends(get_pagination_params),
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = ReportService(db)
    reports = await service.list_reports(current_user.id, skip=pagination.skip, limit=pagination.limit)
    return reports

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report_details(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = ReportService(db)
    report = await service.get_report(report_id, current_user.id)
    if not report:
        raise HTTPException(status_code=404, detail="Medical report not found.")
    return report

@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = ReportService(db)
    success = await service.delete_report(report_id, current_user.id)
    if success:
        return APIResponse.success(message="Report deleted successfully.")
    raise HTTPException(status_code=404, detail="Report not found or permission denied.")
