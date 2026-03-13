import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain.tools import tool
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

@tool
def send_email(input_str: str) -> str:
    """
    Send an email. Input format: 'to@email.com | Subject | Body message'
    Example: 'friend@gmail.com | Meeting tomorrow | Hi, just confirming our meeting at 5pm.'
    """
    try:
        parts = [p.strip() for p in input_str.split("|")]
        if len(parts) != 3:
            return "Format should be: recipient | subject | body"
        to_email, subject, body = parts

        msg = MIMEMultipart()
        msg["From"]    = EMAIL_ADDRESS
        msg["To"]      = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

        return f"Email sent to {to_email} successfully."
    except Exception as e:
        return f"Failed to send email: {str(e)}"