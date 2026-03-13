import pywhatkit
from langchain_core.tools import tool
from logger import get_logger

log = get_logger("tool.whatsapp")


@tool
def send_whatsapp(phone_number: str, message: str) -> str:
    """
    Send a WhatsApp message via WhatsApp Web.
    phone_number: must include country code, e.g. +919876543210.
    message: text to send.
    """
    if not phone_number.startswith("+"):
        return "Phone number must start with country code, e.g. +91..."
    log.info(f"WhatsApp → {phone_number}")
    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_number, message,
            wait_time=12,
            tab_close=True,
            close_time=3,
        )
        return f"WhatsApp message sent to {phone_number}."
    except Exception as e:
        log.error(f"WhatsApp error: {e}")
        return f"WhatsApp failed: {e}"