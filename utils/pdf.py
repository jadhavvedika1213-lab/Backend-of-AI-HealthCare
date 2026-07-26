from pathlib import Path
from pypdf import PdfReader
from core.logger import logger

def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text from PDF pages using pypdf.
    """
    if not pdf_path.exists():
        logger.error(f"PDF file does not exist: {pdf_path}")
        return ""
    
    try:
        reader = PdfReader(pdf_path)
        extracted_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_text.append(text)
        return "\n".join(extracted_text)
    except Exception as e:
        logger.error(f"Error reading PDF {pdf_path}: {str(e)}")
        return ""
