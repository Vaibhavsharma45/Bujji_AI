"""
BUJJI v3 — Central Configuration
All settings live here. Never hardcode values elsewhere.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM ───────────────────────────────────────────────────────────
GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.1-8b-instant"   # fast + small = zyada queries
GROQ_TEMP      = 0
GROQ_MAX_TOKENS= 1024

# ── Identity ───────────────────────────────────────────────────────
BUJJI_NAME     = "BUJJI"
VERSION        = "3.0.0"

# ── Wake Word ──────────────────────────────────────────────────────
PICOVOICE_KEY  = os.getenv("PICOVOICE_KEY", "YOUR_KEY_HERE")
WAKE_WORD      = "jarvis"           # free built-in keyword
WAKE_COOLDOWN  = 2.5               # seconds between detections

# ── Voice ──────────────────────────────────────────────────────────
TTS_RATE       = 165               # words per minute
TTS_VOLUME     = 1.0
STT_LANGUAGE   = "en-IN"
STT_TIMEOUT    = 6                 # seconds to wait for speech start
STT_PHRASE_LIMIT = 15              # max seconds per phrase

# ── Email ──────────────────────────────────────────────────────────
EMAIL_ADDRESS  = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
SMTP_HOST      = "smtp.gmail.com"
SMTP_PORT      = 465

# ── System Monitor ─────────────────────────────────────────────────
MONITOR_CPU_THRESHOLD  = 85        # alert above this %
MONITOR_RAM_THRESHOLD  = 85
MONITOR_BATTERY_LOW    = 15
MONITOR_INTERVAL       = 30        # seconds

# ── Agent ──────────────────────────────────────────────────────────
AGENT_RECURSION_LIMIT  = 6        # max LangGraph steps per query
CHAT_HISTORY_MAX       = 20       # messages to keep in context
MEMORY_RESULTS         = 3        # past memories to inject

# ── Paths ──────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
LOG_FILE   = os.path.join(BASE_DIR, "logs", "bujji.log")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

# ── FastAPI ────────────────────────────────────────────────────────
API_HOST   = "0.0.0.0"
API_PORT   = 8000


def validate() -> bool:
    """Check required env vars at startup. Warn but don't crash."""
    warnings = []
    if not GROQ_API_KEY:
        warnings.append("GROQ_API_KEY missing — LLM will not work")
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        warnings.append("EMAIL_ADDRESS / EMAIL_PASSWORD missing — email disabled")
    if PICOVOICE_KEY == "YOUR_KEY_HERE":
        warnings.append("PICOVOICE_KEY missing — wake word disabled (use voice/text mode)")
    for w in warnings:
        print(f"  [!] {w}")
    return len(warnings) == 0