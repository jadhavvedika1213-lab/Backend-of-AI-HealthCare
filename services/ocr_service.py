from pathlib import Path
from utils.ocr import perform_ocr_on_image
from utils.pdf import extract_text_from_pdf
from utils.helpers import get_file_extension
from core.config import settings

class OCRService:
    @staticmethod
    async def extract_text(file_path_str: str) -> str:
        """
        Identify file type and extract text.
        """
        abs_path = settings.get_absolute_path(file_path_str)
        ext = get_file_extension(abs_path.name)
        
        if ext == ".pdf":
            # PDF text extraction
            return extract_text_from_pdf(abs_path)
        elif ext in {".png", ".jpg", ".jpeg"}:
            # Image OCR extraction via Gemini multimodal
            return perform_ocr_on_image(abs_path)
        
        return ""
