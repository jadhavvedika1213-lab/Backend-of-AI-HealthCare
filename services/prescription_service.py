import json
from models.prescription import Prescription
from models.medicine import Medicine
from services.ocr_service import OCRService
import google.generativeai as genai
from core.config import settings
from utils.prompt import MedicalPrompts
from core.logger import logger
from typing import List, Optional

class PrescriptionService:
    def __init__(self, db):
        self.db = db

    async def create_prescription(self, user_id: int, file_path: str) -> Prescription:
        # 1. OCR text extraction
        raw_text = await OCRService.extract_text(file_path)
        
        # 2. Parse details using Gemini API
        doctor_name = "Unknown Doctor"
        clinic_name = "Unknown Clinic"
        medicines_list = []
        summary = ""

        if "YOUR_GEMINI_API_KEY" in settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY:
            # Fallback mock parsing
            doctor_name = "Dr. John Doe"
            clinic_name = "City Health Clinic"
            summary = "Prescribed Amoxicillin for bacterial infection."
            medicines_list = [
                {
                    "name": "Amoxicillin",
                    "dosage": "500mg",
                    "frequency": "Three times daily",
                    "duration": "7 days",
                    "instructions": "Take after meals"
                }
            ]
        else:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # Request structured JSON format
                parse_prompt = (
                    "Analyze the following medical prescription text and extract structured information. "
                    "You must respond in valid JSON format only, matching the schema: "
                    "{\n"
                    "  \"doctor_name\": \"string or null\",\n"
                    "  \"clinic_name\": \"string or null\",\n"
                    "  \"summary\": \"brief summary of prescription instructions\",\n"
                    "  \"medicines\": [\n"
                    "     {\"name\": \"string\", \"dosage\": \"string\", \"frequency\": \"string\", \"duration\": \"string\", \"instructions\": \"string\"}\n"
                    "  ]\n"
                    "}\n"
                    f"Prescription content:\n{raw_text}"
                )
                
                response = model.generate_content(parse_prompt)
                res_text = response.text.strip()
                
                # Strip markdown code blocks if Gemini returns ```json ... ```
                if res_text.startswith("```json"):
                    res_text = res_text[7:]
                if res_text.endswith("```"):
                    res_text = res_text[:-3]
                res_text = res_text.strip()
                
                parsed = json.loads(res_text)
                doctor_name = parsed.get("doctor_name", "Unknown Doctor")
                clinic_name = parsed.get("clinic_name", "Unknown Clinic")
                summary = parsed.get("summary", "")
                medicines_list = parsed.get("medicines", [])
            except Exception as e:
                logger.error(f"Failed to parse prescription with Gemini: {str(e)}")
                summary = "Failed to auto-parse details via AI. Raw text captured."

        # Create Prescription record
        prescription = Prescription(
            user_id=user_id,
            file_path=file_path,
            doctor_name=doctor_name,
            clinic_name=clinic_name,
            raw_text=raw_text,
            summary=summary
        )
        self.db.add(prescription)
        await self.db.commit()
        await self.db.refresh(prescription)

        # Create related medicines
        for med_data in medicines_list:
            medicine = Medicine(
                prescription_id=prescription.id,
                name=med_data.get("name", "Unknown Medicine"),
                dosage=med_data.get("dosage"),
                frequency=med_data.get("frequency"),
                duration=med_data.get("duration"),
                instructions=med_data.get("instructions")
            )
            self.db.add(medicine)
        
        await self.db.commit()
        
        # Re-fetch prescription with medicines relationship
        result = await self.db.execute(
            select(Prescription)
            .filter(Prescription.id == prescription.id)
            .options(selectinload(Prescription.medicines))
        )
        return result.scalars().first()

    async def get_by_user_id(self, user_id: int) -> List[Prescription]:
        result = await self.db.execute(
            select(Prescription)
            .filter(Prescription.user_id == user_id)
            .options(selectinload(Prescription.medicines))
        )
        return list(result.scalars().all())

    async def get_by_id(self, prescription_id: int) -> Optional[Prescription]:
        result = await self.db.execute(
            select(Prescription)
            .filter(Prescription.id == prescription_id)
            .options(selectinload(Prescription.medicines))
        )
        return result.scalars().first()
        
    async def delete(self, prescription_id: int) -> bool:
        prescription = await self.get_by_id(prescription_id)
        if not prescription:
            return False
        await self.db.delete(prescription)
        await self.db.commit()
        return True
