import os
from pathlib import Path
from fastapi import UploadFile
from core.config import settings
from utils.helpers import ensure_dir_exists, generate_uuid, get_file_extension, is_allowed_file
from exceptions.custom import BaseHealthcareException

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

class UploadService:
    @staticmethod
    async def save_uploaded_file(file: UploadFile, subfolder: str) -> str:
        """
        Saves file to static subdirectory and returns the relative path.
        """
        ext = get_file_extension(file.filename)
        if ext not in ALLOWED_EXTENSIONS:
            raise BaseHealthcareException(f"Unsupported file format {ext}. Allowed formats: PDF, PNG, JPG, JPEG")

        # Ensure target folder exists
        folder_path = ensure_dir_exists(subfolder)
        
        # Create a unique filename
        unique_name = f"{generate_uuid()}{ext}"
        destination = folder_path / unique_name

        try:
            # Read and save file content
            content = await file.read()
            with open(destination, "wb") as f:
                f.write(content)
            
            # Return relative path for web access
            # e.g., 'static/uploads/unique_name.pdf'
            # Convert Windows path backslashes to forward slashes for URL routing
            relative_path = os.path.relpath(destination, settings.ROOT_DIR)
            return relative_path.replace("\\", "/")
        except Exception as e:
            raise BaseHealthcareException(f"Failed to write file to disk: {str(e)}")
