import os
import uuid
from pathlib import Path
from core.config import settings

def generate_uuid() -> str:
    return str(uuid.uuid4())

def ensure_dir_exists(directory_path: str) -> Path:
    path = settings.get_absolute_path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

def is_allowed_file(filename: str, allowed_extensions: set) -> bool:
    ext = get_file_extension(filename)
    return ext in allowed_extensions
