import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio
from concurrent.futures import ThreadPoolExecutor
from core.config import settings
from core.logger import logger

executor = ThreadPoolExecutor(max_workers=3)

def _send_smtp_email(to_email: str, subject: str, html_content: str) -> None:
    # Check if SMTP details are placeholder
    if "your-email" in settings.SMTP_USER or not settings.SMTP_USER:
        logger.info(
            f"=== [SMTP MOCK] Email Sent ==="
            f"\nTo: {to_email}"
            f"\nSubject: {subject}"
            f"\nContent Summary: {html_content[:200]}..."
            f"\n==============================="
        )
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email

    part = MIMEText(html_content, "html")
    msg.attach(part)

    try:
        # Connect to SMTP
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_FROM, to_email, msg.as_string())
        server.quit()
        logger.info(f"Successfully sent email to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email} via SMTP: {str(e)}")
        raise e

async def send_email(to_email: str, subject: str, html_content: str) -> None:
    """
    Run SMTP sending asynchronously using ThreadPoolExecutor.
    """
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(executor, _send_smtp_email, to_email, subject, html_content)
