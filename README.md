# BUJJI — FRIDAY Edition 🤖

> **Your personal JARVIS. Voice-controlled. Emotion-aware. Fully offline wake word.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-ReAct-green?style=flat-square)](https://github.com/langchain-ai/langgraph)
[![Groq](https://img.shields.io/badge/Groq-llama--3.3--70b-orange?style=flat-square)](https://console.groq.com)
[![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)](LICENSE)

---

## What is BUJJI?

BUJJI is a personal AI voice assistant built for Windows — inspired by JARVIS from Iron Man. Say **"Hey Robo"** and BUJJI wakes up, listens, thinks, and acts. It can open apps, search the web, send emails, control your PC volume, lock your screen, set reminders, and a lot more — all hands-free.

---

## Demo

```
You say:  "Hey Robo"
FRIDAY:   "Haan bhaiya, bolo!"

You say:  "Open YouTube"
FRIDAY:   "Lo khulja YouTube bhaiya!"

You say:  "Volume 60 karo"
FRIDAY:   "Volume 60% set bhaiya."

You say:  "Search latest AI news"
FRIDAY:   "Yeh raha bhaiya — OpenAI ne..."

You say:  "Set reminder at 18:00 chai peeni hai"
FRIDAY:   "Reminder set bhaiya, 6 baje yaad dilaaunga!"
```

---

## Features

| Feature | Description |
|---|---|
| 🎙️ Custom Wake Word | Offline "Hey Robo" detection via Picovoice Porcupine |
| 🧠 AI Brain | Groq llama-3.3-70b-versatile via LangGraph ReAct agent |
| 💾 Persistent Memory | ChromaDB vector store — remembers past conversations |
| 😤 Emotion Detection | librosa voice analysis — adapts tone to your mood |
| 🌐 Web Search | DuckDuckGo text + news search |
| 💻 PC Control | Open 30+ apps/sites, screenshot, clipboard, kill process |
| 🔊 Volume Control | Set system volume, mute/unmute via voice |
| 🔒 Screen Lock | Lock Windows instantly by voice |
| 📧 Email | Send Gmail with attachments |
| 💬 WhatsApp | Send messages via WhatsApp Web |
| ⏰ Reminders | Voice reminders — once, daily, hourly |
| 🧮 Calculator | Math, unit conversion, date/time |
| 📊 System Monitor | Background CPU/RAM/battery alerts |
| 🌐 Autonomous Browser | Real browser automation via Playwright |
| 🖥️ REST API | FastAPI server at localhost:8000 |
| 🎨 Rich CLI | Beautiful terminal UI with colors |

---

## Tech Stack — 100% Free

| Component | Technology |
|---|---|
| LLM | Groq — llama-3.3-70b-versatile (free tier) |
| Agent | LangGraph create_react_agent |
| Wake Word | Picovoice Porcupine (free tier, custom model) |
| Speech Recognition | Google Speech Recognition |
| Text-to-Speech | pyttsx3 (offline) |
| Memory | ChromaDB (local vector store) |
| Web Search | DuckDuckGo (ddgs) |
| Browser Automation | Playwright (Chromium) |
| Emotion Analysis | librosa (signal processing) |
| API | FastAPI + uvicorn |
| CLI | Rich |

---

## Project Structure

```
Bujji_AI/
├── main.py               # Entry point — wake/voice/text modes
├── brain.py              # LangGraph agent + FRIDAY personality
├── voice.py              # TTS (pyttsx3) + STT (Google)
├── wake.py               # Picovoice wake word detection
├── memory.py             # ChromaDB vector memory
├── config.py             # All settings + .env loader
├── logger.py             # Structured logging
├── hey_bujji.ppn         # Custom wake word model (Picovoice)
│
├── tools/
│   ├── search.py         # DuckDuckGo web + news
│   ├── pc_control.py     # Apps, files, screenshot, clipboard
│   ├── email_tool.py     # Gmail SMTP
│   ├── whatsapp.py       # pywhatkit WhatsApp
│   ├── monitor.py        # Background system monitor
│   ├── reminder.py       # Voice reminders (schedule)
│   ├── calculator.py     # Math, units, datetime
│   ├── emotion.py        # Voice emotion detection
│   ├── self_assistance.py # Volume, lock, type, keyboard
│   ├── screen_reader.py  # OCR screen reading (pytesseract)
│   ├── spotify_control.py # Spotify playback control
│   ├── whatsapp_reader.py # WhatsApp message reader
│   └── autonomous_agent.py # Playwright browser automation
│
├── api/
│   └── server.py         # FastAPI REST API
│
├── ui/
│   └── dashboard.html    # Real-time web dashboard
│
├── logs/
│   └── bujji.log         # Structured logs
│
├── .env                  # Your API keys (not in git)
├── .env.example          # Template
└── requirements.txt      # All dependencies
```

---

## Setup

### 1. Clone

```bash
git clone https://github.com/Vaibhavsharma45/Bujji_AI.git
cd Bujji_AI
```

### 2. Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 4. Configure Keys

```bash
copy .env.example .env
```

Open `.env` and fill:

```env
GROQ_API_KEY=your_groq_key        # console.groq.com — free
PICOVOICE_KEY=your_picovoice_key  # console.picovoice.ai — free
EMAIL_ADDRESS=your@gmail.com
EMAIL_PASSWORD=16_char_app_password
```

**Gmail App Password:** [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

### 5. Custom Wake Word (Optional)

1. Go to [console.picovoice.ai](https://console.picovoice.ai)
2. Wake Word → Train → type `hey bujji` or any phrase
3. Platform → **Windows (x86_64, arm64)**
4. Download `.ppn` file
5. Rename to `hey_bujji.ppn` and place in project root

### 6. Run

```bash
python main.py
```

---

## Usage

Select a mode on startup:

| Mode | How to use |
|---|---|
| `w` — Wake word | Say your wake phrase, then speak command |
| `v` — Voice | Speak directly anytime |
| `t` — Text | Type commands in terminal |

### Voice Commands

```bash
# Apps
"open youtube"              → Opens YouTube in browser
"open whatsapp"             → Opens WhatsApp Web
"open vscode"               → Launches VS Code

# System
"volume 70 karo"            → Sets volume to 70%
"mute karo"                 → Toggles mute
"screen lock karo"          → Locks Windows
"system info batao"         → CPU, RAM, disk, battery

# Search & Web
"search latest AI news"     → DuckDuckGo web search
"news about India"          → DuckDuckGo news
"play Arijit Singh youtube" → Opens YouTube and plays

# Productivity
"set reminder at 18:00 chai peeni hai"  → Voice reminder at 6 PM
"calculate 25% of 4500"                 → 1125.0
"convert 10 km to miles"                → 6.2137 miles
"time kya hai"                          → Current time (instant)

# Communication
"send email to a@b.com subject Hi body Hello"  → Sends Gmail
"send whatsapp to +91XXXXXXXXXX message Hello" → WhatsApp

# Memory
"clear memory"              → Wipes conversation memory
"memory stats"              → How many memories stored

# Exit
"bye" / "exit" / "band kar" → Shuts down BUJJI
```

---

## REST API

Start the API server:

```bash
uvicorn api.server:app --reload
```

Then open **[http://localhost:8000](http://localhost:8000)** — real-time dashboard with chat UI and live system stats.

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Web dashboard |
| `/ask` | POST | Send query to BUJJI |
| `/stats` | GET | CPU, RAM, battery, memory count |
| `/health` | GET | API status |
| `/memory` | DELETE | Clear memory |
| `/history` | DELETE | Clear chat history |

---

## Built By

**Vaibhav Sharma**
GitHub: [@Vaibhavsharma45](https://github.com/Vaibhavsharma45)

---

*"Not just a project — it's a personal AI that actually works."*