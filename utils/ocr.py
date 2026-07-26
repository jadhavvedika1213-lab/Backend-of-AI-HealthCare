import os
from pathlib import Path
import google.generativeai as genai
from core.config import settings
from core.logger import logger
from PIL import Image

def perform_ocr_on_image(image_path: Path) -> str:
    """
    Perform OCR on a medical document image using the Gemini API.
    """
    if "YOUR_GEMINI_API_KEY" in settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY:
        logger.warning("Gemini API key is not configured. Falling back to Mock OCR.")
        return "[MOCK OCR CONTENT] Sample medical record text: Blood Pressure 120/80 mmHg, Pulse 72 bpm, Cholesterol 210 mg/dL, HbA1c 5.8%."

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Load image
        img = Image.open(image_path)
        
        prompt = (
            "You are a specialized medical OCR engine. Transcribe all text, numbers, and handwritten notes "
            "found in this medical document image as accurately as possible. Output only the transcript text."
        )
        
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        logger.error(f"Gemini OCR extraction failed: {str(e)}")
        # Return fallback text rather than crashing
        return f"[OCR ERROR: {str(e)}]"
