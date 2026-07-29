from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.upload_service import UploadService
from services.image_service import ImageService
from core.config import settings
from utils.response import APIResponse

router = APIRouter()

@router.post("/interactive")
async def interactive_read_mi(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    current_user: User = Depends(get_current_active_user)
):
    # Save file
    path = await UploadService.save_uploaded_file(file, settings.IMAGES_DIR)

    # Process with ImageService
    analysis = await ImageService.interactive_read_medical_image(path, prompt)

    return APIResponse.success(
        message="Medical scan analyzed interactively.",
        data={
            "filename": file.filename,
            "file_url": f"/{path}",
            "prompt": prompt,
            "analysis": analysis
        }
    )

@router.post("/analyze")
async def analyze_scan(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    # Save file
    path = await UploadService.save_uploaded_file(file, settings.IMAGES_DIR)
    
    # Process with ImageService
    analysis = await ImageService.analyze_medical_image(path)
    
    return APIResponse.success(
        message="Medical scan analyzed successfully.",
        data={
            "filename": file.filename,
            "file_url": f"/{path}",
            "analysis": analysis
        }
    )
