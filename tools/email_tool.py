"""
tools/email_tool.py — Gmail integration
Supports plain text, HTML emails, and file attachments.
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from langchain_core.tools import tool
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_HOST, SMTP_PORT
from logger import get_logger

log = get_logger("tool.email")


def _build_message(to: str, subject: str, body: str, attachment_path: str = "") -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"]    = EMAIL_ADDRESS
    msg["To"]      = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    if attachment_path and os.path.isfile(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(attachment_path)}"
        )
        msg.attach(part)
    return msg


@tool
def send_email(to: str, subject: str, body: str, attachment_path: str = "") -> str:
    """
    Send an email via Gmail.
    to: recipient email (e.g. someone@gmail.com).
    subject: email subject line.
    body: email body text.
    attachment_path: optional full path to file to attach.
    """
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return "Email not configured. Set EMAIL_ADDRESS and EMAIL_PASSWORD in .env"
    if not to or "@" not in to:
        return "Invalid email address."

    log.info(f"Sending email → {to}: {subject}")
    try:
        msg = _build_message(to, subject, body, attachment_path)
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to, msg.as_string())
        return f"Email sent to {to}."
    except smtplib.SMTPAuthenticationError:
        return "Gmail auth failed. Use 16-char App Password from myaccount.google.com/apppasswords"
    except smtplib.SMTPException as e:
        log.error(f"SMTP error: {e}")
        return f"Email failed: {e}"
    except Exception as e:
        log.error(f"Email error: {e}")
        return f"Email error: {e}"