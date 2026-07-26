from utils.email import send_email
from core.logger import logger

class EmailService:
    @staticmethod
    async def send_welcome_email(email: str, name: str) -> None:
        subject = "Welcome to AI HealthCare"
        html = (
            f"<h2>Hello {name or 'Health User'},</h2>"
            f"<p>Thank you for signing up for AI HealthCare Backend. We are excited to support you on your wellness journey!</p>"
            f"<p>You can now upload medical reports, configure reminders, and chat with HealthBuddy, your AI medical companion.</p>"
        )
        await send_email(email, subject, html)

    @staticmethod
    async def send_reminder_email(email: str, name: str, reminder_title: str, reminder_time: str) -> None:
        subject = f"Health Reminder: {reminder_title}"
        html = (
            f"<h2>Hello {name or 'Patient'},</h2>"
            f"<p>This is a friendly reminder that you have a scheduled task:</p>"
            f"<h3><strong>{reminder_title}</strong> at <strong>{reminder_time}</strong></h3>"
            f"<p>Please ensure you log your completion in the app.</p>"
        )
        await send_email(email, subject, html)

    @staticmethod
    async def send_report_ready_email(email: str, filename: str) -> None:
        subject = f"Medical Report Analyzed: {filename}"
        html = (
            f"<h2>Medical Report Ready</h2>"
            f"<p>Your uploaded document <strong>{filename}</strong> has been successfully processed and analyzed by our AI system.</p>"
            f"<p>Log in to your portal to review findings and recommendations.</p>"
        )
        await send_email(email, subject, html)
