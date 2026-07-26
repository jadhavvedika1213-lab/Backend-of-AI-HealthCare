from pathlib import Path
from PIL import Image
import google.generativeai as genai
from core.config import settings
from utils.prompt import MedicalPrompts
from core.logger import logger

class ImageService:
    @staticmethod
    async def analyze_medical_image(image_path_str: str) -> str:
        """
        Analyze medical image (X-Ray, MRI) using Gemini Multimodal.
        """
        abs_path = settings.get_absolute_path(image_path_str)
        if not abs_path.exists():
            return "Error: Image file not found on disk."
            
        if "YOUR_GEMINI_API_KEY" in settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY:
            logger.warning("Gemini API key is not configured. Returning Mock Image Analysis.")
            return (
                "### Mock Image Analysis Report\n"
                "**Type**: Chest X-Ray (AP View)\n"
                "**Observations**: Lungs appear clear without focal consolidation. Cardiac silhouette is within normal limits. Bone structures appear intact.\n"
                "**Impression**: No acute cardiopulmonary abnormality detected.\n"
                "**Disclaimer**: This is a mock analysis for demo purposes. Consult a certified radiologist."
            )
            
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # Load PIL Image
            img = Image.open(abs_path)
            
            response = model.generate_content([MedicalPrompts.IMAGE_ANALYSIS, img])
            return response.text
        except Exception as e:
            logger.error(f"Image analysis via Gemini failed: {str(e)}")
            return f"Error during image analysis: {str(e)}"
class ImageAnalysisService(ImageService):
    pass
