import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")      # Free at console.groq.com
GROQ_MODEL   = "llama3-70b-8192"                   # Fast & free

EMAIL_ADDRESS  = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")   # Gmail app password

JARVIS_NAME = "JARVIS"
WAKE_WORD   = "jarvis"