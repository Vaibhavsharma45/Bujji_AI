# BUJJI — Personal AI Voice Assistant

> *"Your personal JARVIS — voice-controlled, emotion-aware, fully offline capable."*

A production-grade AI assistant built with LangGraph, Groq, pvporcupine, and ChromaDB. Supports offline wake word detection, voice emotion analysis, persistent memory, PC automation, email, WhatsApp, system monitoring, and reminders — all on a 100% free stack.

---

## Features

| Category | What it does |
|---|---|
| Wake Word | Offline detection via pvporcupine ("Jarvis") |
| Voice I/O | Speech recognition (Google) + pyttsx3 TTS |
| Emotion Detection | librosa pitch/energy analysis → tone-aware responses |
| LLM | Groq llama-3.3-70b-versatile (free tier) |
| Agent | LangGraph ReAct with 17 tools |
| Memory | ChromaDB vector store — persists across sessions |
| PC Control | Open 30+ apps/sites, files, screenshot, clipboard, kill process |
| Email | Gmail with attachment support |
| WhatsApp | Send messages via WhatsApp Web |
| System Monitor | Background CPU/RAM/battery alerts |
| Reminders | Voice reminders — once / daily / hourly |
| Calculator | Math, unit conversion, date/time |
| News Search | DuckDuckGo web + news search |
| REST API | FastAPI server at localhost:8000 |
| CLI | Rich terminal UI with color output |

---

## Setup

### 1. Clone and create virtualenv
```bash
git clone https://github.com/Vaibhavsharma45/Bujji_AI.git
cd Bujji_AI
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Open .env and fill in your keys
```

**Required keys:**

| Key | Where to get |
|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) — free |
| `PICOVOICE_KEY` | [console.picovoice.ai](https://console.picovoice.ai) — free |
| `EMAIL_ADDRESS` | Your Gmail address |
| `EMAIL_PASSWORD` | [App Password](https://myaccount.google.com/apppasswords) — 16 chars |

### 4. Run
```bash
python main.py
```

---

## Usage

```
Mode: [w] Wake word / [v] Voice / [t] Text
```

### Voice commands (examples)

```
open youtube          → opens YouTube in browser
open gmail            → opens Gmail
search latest AI news → DuckDuckGo web search
news about india      → DuckDuckGo news search
system info           → CPU, RAM, disk, battery
top processes         → top 5 CPU processes
monitor start         → background CPU/RAM alerts
set reminder at 14:30 remind me to drink water → voice reminder
calculate 25% of 4500 → 1125.0
convert 10 km to miles → 6.2137 miles
send email to a@b.com subject Test body Hello → sends email
send whatsapp to +919876543210 message Hello  → WhatsApp
clear memory          → wipe ChromaDB store
time / date           → instant response, no LLM
```

---

## Architecture

```
main.py          Entry point, mode selection, rich CLI
brain.py         LangGraph ReAct agent, emotion-aware prompt
voice.py         TTS (subprocess-isolated) + STT
wake.py          pvporcupine offline wake word
memory.py        ChromaDB vector memory
config.py        Central config + .env loader
logger.py        File + console structured logging

tools/
  search.py      DuckDuckGo text + news
  pc_control.py  App launcher, files, screenshot, clipboard, processes
  email_tool.py  Gmail SMTP with attachments
  whatsapp.py    pywhatkit WhatsApp Web
  monitor.py     Background CPU/RAM/battery monitor
  reminder.py    schedule-based voice reminders
  calculator.py  Math, unit conversion, date/time
  emotion.py     librosa voice emotion detection

api/
  server.py      FastAPI REST API
```

---

## REST API

Start the API server:
```bash
uvicorn api.server:app --reload
```

Endpoints:
```
GET  /health          → status check
POST /ask             → { "query": "...", "emotion": "neutral" }
GET  /memory/stats    → memory count
DELETE /memory        → clear all memory
DELETE /history       → clear chat history
```

---

## Tech Stack (100% Free)

- **LLM**: Groq llama-3.3-70b-versatile
- **Agent**: LangGraph create_react_agent
- **Wake Word**: pvporcupine (Picovoice free tier)
- **STT**: Google Speech Recognition
- **TTS**: pyttsx3 (offline)
- **Memory**: ChromaDB (local)
- **Search**: DuckDuckGo (ddgs)
- **Email**: smtplib / Gmail
- **WhatsApp**: pywhatkit
- **Emotion**: librosa
- **API**: FastAPI
- **CLI**: Rich

---

*Built by Vaibhav Sharma*