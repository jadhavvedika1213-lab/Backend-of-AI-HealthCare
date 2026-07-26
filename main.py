from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from core.config import settings
from core.startup import run_startup_tasks
from core.shutdown import run_shutdown_tasks
from core.middlewares import register_middleware
from exceptions.handlers import register_exception_handlers

# Import Routers
from api.v1 import (
    health, auth, profile, settings as user_settings, users, dashboard,
    upload, pdf, prescription, medical_image, ocr, ai, chatbot, rag,
    reminder, reports, history, analytics, voice, notification, search,
    feedback, admin
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    await run_startup_tasks()
    yield
    # Shutdown tasks
    await run_shutdown_tasks()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Backend API for AI Healthcare companion, handling medical scans, OCR, AI advice, and reminders.",
    lifespan=lifespan
)

# Register Custom Middlewares
register_middleware(app)

# Register Custom Exception Handlers
register_exception_handlers(app)

# Mount Static Files for direct uploads lookup
# Ensure static folder is available or create it
settings.get_absolute_path("static").mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(settings.get_absolute_path("static"))), name="static")

# Register Routers (under v1 namespace)
api_prefix = "/api/v1"
app.include_router(health.router, prefix=f"{api_prefix}/health", tags=["Health"])
app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["Authentication"])
app.include_router(profile.router, prefix=f"{api_prefix}/profile", tags=["User Profile"])
app.include_router(user_settings.router, prefix=f"{api_prefix}/settings", tags=["User Settings"])
app.include_router(users.router, prefix=f"{api_prefix}/users", tags=["Users Directory"])
app.include_router(dashboard.router, prefix=f"{api_prefix}/dashboard", tags=["Dashboard"])
app.include_router(upload.router, prefix=f"{api_prefix}/upload", tags=["Upload Service"])
app.include_router(pdf.router, prefix=f"{api_prefix}/pdf", tags=["PDF Processing & Analysis"])
app.include_router(prescription.router, prefix=f"{api_prefix}/prescription", tags=["Prescription Management"])
app.include_router(medical_image.router, prefix=f"{api_prefix}/medical_image", tags=["Medical Image Analysis"])
app.include_router(ocr.router, prefix=f"{api_prefix}/ocr", tags=["OCR Transcription"])
app.include_router(ai.router, prefix=f"{api_prefix}/ai", tags=["AI Queries"])
app.include_router(chatbot.router, prefix=f"{api_prefix}/chatbot", tags=["Chatbot Companion"])
app.include_router(rag.router, prefix=f"{api_prefix}/rag", tags=["RAG Document Knowledge base"])
app.include_router(reminder.router, prefix=f"{api_prefix}/reminder", tags=["Reminders Alert"])
app.include_router(reports.router, prefix=f"{api_prefix}/reports", tags=["Reports Management"])
app.include_router(history.router, prefix=f"{api_prefix}/history", tags=["Patient Health History"])
app.include_router(analytics.router, prefix=f"{api_prefix}/analytics", tags=["Telemetry Analytics"])
app.include_router(voice.router, prefix=f"{api_prefix}/voice", tags=["Voice Transcription & TTS"])
app.include_router(notification.router, prefix=f"{api_prefix}/notification", tags=["In-App Notifications"])
app.include_router(search.router, prefix=f"{api_prefix}/search", tags=["Global Database Search"])
app.include_router(feedback.router, prefix=f"{api_prefix}/feedback", tags=["User Feedback"])
app.include_router(admin.router, prefix=f"{api_prefix}/admin", tags=["Administrator Controls"])

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "docs_url": "/docs"
    }
