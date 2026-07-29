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

    @staticmethod
    async def interactive_read_medical_image(image_path_str: str, prompt: str) -> str:
        """
        Interactively read/analyze medical image (X-Ray, MRI) using Gemini Multimodal with a custom user prompt.
        """
        abs_path = settings.get_absolute_path(image_path_str)
        if not abs_path.exists():
            return "Error: Image file not found on disk."

        if "YOUR_GEMINI_API_KEY" in settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY:
            logger.warning("Gemini API key is not configured. Returning Mock Interactive Image Analysis.")
            return (
                f"### Mock Interactive Image Analysis Report\n"
                f"**User Prompt**: {prompt}\n"
                f"**Analysis**: This is a mock interactive analysis addressing your query about the medical image.\n"
                f"**Disclaimer**: This is a mock analysis for demo purposes. Consult a certified professional."
            )

        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Load PIL Image
            img = Image.open(abs_path)

            full_prompt = (
                f"You are an expert medical radiologist. The user has provided an image and asked: '{prompt}'.\n"
                f"Examine the image carefully and answer the user's question accurately, clearly, and objectively.\n"
                f"Always include a disclaimer indicating this is for screening/educational purposes, not official diagnosis."
            )

            response = model.generate_content([full_prompt, img])
            return response.text
        except Exception as e:
            logger.error(f"Interactive image analysis via Gemini failed: {str(e)}")
            return f"Error during interactive image analysis: {str(e)}"
class ImageAnalysisService(ImageService):
    pass
