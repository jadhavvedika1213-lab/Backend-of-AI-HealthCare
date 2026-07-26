from utils.prompt import MedicalPrompts

# Re-exporting for import simplicity in case files reference ai/prompts.py
REPORT_ANALYSIS_PROMPT = MedicalPrompts.REPORT_ANALYSIS
IMAGE_ANALYSIS_PROMPT = MedicalPrompts.IMAGE_ANALYSIS
PRESCRIPTION_PROMPT = MedicalPrompts.PRESCRIPTION_EXPLANATION
CHATBOT_PROMPT = MedicalPrompts.CHATBOT_SYSTEM
RAG_PROMPT = MedicalPrompts.RAG_CONTEXT_PROMPT
