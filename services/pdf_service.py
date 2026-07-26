from models.report import Report
from repositories.report_repo import ReportRepository
from services.ocr_service import OCRService
import google.generativeai as genai
from core.config import settings
from utils.prompt import MedicalPrompts
from core.logger import logger

class PDFService:
    def __init__(self, db):
        self.repo = ReportRepository(db)

    async def process_and_analyze_report(self, report_id: int) -> Report:
        report = await self.repo.get_by_id(report_id)
        if not report:
            raise Exception("Report not found")
        
        # 1. OCR text extraction
        extracted_text = await OCRService.extract_text(report.file_path)
        report.ocr_content = extracted_text
        
        # 2. Analyze extracted text using Gemini API
        if "YOUR_GEMINI_API_KEY" in settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY:
            # Fallback mock analysis
            report.summary = "Mock Report Summary: Patient shows typical metrics with slightly elevated cholesterol levels."
            report.analysis_result = (
                "Mock Analysis Result:\n"
                "- Vitals look stable.\n"
                "- Cholesterol: 210 mg/dL (Borderline High - recommend reducing saturated fats).\n"
                "- Advice: Hydrate well, exercise, and discuss details with your GP."
            )
        else:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # Fetch Summary
                summary_prompt = f"Summarize this medical report in 2-3 sentences:\n\n{extracted_text}"
                summary_response = model.generate_content(summary_prompt)
                report.summary = summary_response.text
                
                # Fetch Full Analysis
                analysis_prompt = MedicalPrompts.REPORT_ANALYSIS.format(report_content=extracted_text)
                analysis_response = model.generate_content(analysis_prompt)
                report.analysis_result = analysis_response.text
                
            except Exception as e:
                logger.error(f"Gemini API report analysis failed: {str(e)}")
                report.summary = "Analysis currently unavailable (API Error)"
                report.analysis_result = f"Error during AI analysis: {str(e)}"
        
        # Save updates to DB
        return await self.repo.update(report)
