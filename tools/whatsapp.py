import pywhatkit
from langchain.tools import tool

@tool
def send_whatsapp(input_str: str) -> str:
    """
    Send a WhatsApp message. Input format: '+91XXXXXXXXXX | Your message here'
    Phone number must include country code. Example: '+919876543210 | Hello bhai!'
    Note: WhatsApp Web must be open in Chrome.
    """
    try:
        parts = [p.strip() for p in input_str.split("|")]
        if len(parts) != 2:
            return "Format: phone_number | message"
        phone, message = parts

        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=10,
            tab_close=True
        )
        return f"WhatsApp message sent to {phone}."
    except Exception as e:
        return f"WhatsApp send failed: {str(e)}"