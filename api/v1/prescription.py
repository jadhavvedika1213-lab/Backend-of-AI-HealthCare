from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.upload_service import UploadService
from services.prescription_service import PrescriptionService
from core.config import settings
from core.database import get_db
from utils.response import APIResponse
from schemas.prescription import PrescriptionResponse
from typing import List

router = APIRouter()

@router.post("/upload")
async def upload_prescription(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    # Save file to prescriptions directory
    path = await UploadService.save_uploaded_file(file, settings.PRESCRIPTION_DIR)
    
    # Process
    service = PrescriptionService(db)
    prescription = await service.create_prescription(current_user.id, path)
    
    return APIResponse.success(
        message="Prescription uploaded and parsed successfully.",
        data=PrescriptionResponse.model_validate(prescription)
    )

@router.get("", response_model=List[PrescriptionResponse])
async def list_prescriptions(
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = PrescriptionService(db)
    items = await service.get_by_user_id(current_user.id)
    return items

@router.delete("/{prescription_id}")
async def delete_prescription(
    prescription_id: int,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = PrescriptionService(db)
    success = await service.delete(prescription_id)
    if success:
        return APIResponse.success(message="Prescription deleted successfully.")
    raise HTTPException(status_code=404, detail="Prescription not found.")
