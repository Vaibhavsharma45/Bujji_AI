<div align="center">

# 🤖 BUJJI — FRIDAY Edition

### Your Personal AI Voice Assistant

*Say **"Hey Robo"** → BUJJI wakes up → Listens → Acts*

<br>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-FF6B35?style=for-the-badge)](https://console.groq.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-ReAct_Agent-00C896?style=for-the-badge)](https://github.com/langchain-ai/langgraph)
[![License](https://img.shields.io/badge/License-MIT-9B59B6?style=for-the-badge)](LICENSE)

<br>

</div>

---

## 📸 Screenshots

<div align="center">

<!-- Replace these with your actual screenshot paths after pushing to GitHub -->

| Wake Word Active | Voice Command | Dashboard |
|:---:|:---:|:---:|
| ![Wake]([assets/screenshots/demo1.png](https://github.com/Vaibhavsharma45/Bujji_AI/blob/main/assets/screenshot/demo1.png)) | ![Voice](assets/screenshots/demo2.png) | ![Dashboard](assets/screenshots/demo3.png) |

</div>

---

## ✨ What can BUJJI do?

> Think of it as your own JARVIS — running 100% on your laptop, no subscription needed.

```
🗣  You  →  "Hey Robo... open YouTube"
🤖  BUJJI →  "Lo khulja YouTube bhaiya!"  ✅

🗣  You  →  "Hey Robo... volume 60 karo"
🤖  BUJJI →  "Volume 60% set bhaiya."     ✅

🗣  You  →  "Hey Robo... search latest AI news"
🤖  BUJJI →  "Yeh raha bhaiya..."          ✅

🗣  You  →  "Hey Robo... remind me at 6pm chai"
🤖  BUJJI →  "Reminder set bhaiya!"        ✅
```

---

## 🚀 Features

| | Feature | Details |
|---|---|---|
| 🎙️ | **Custom Wake Word** | Offline "Hey Robo" — no internet needed to wake |
| 🧠 | **AI Brain** | LLaMA 3.3 70B via Groq (free tier) |
| 💾 | **Memory** | Remembers past conversations (ChromaDB) |
| 😤 | **Emotion Detection** | Adapts tone based on your voice mood |
| 💻 | **PC Control** | Open 30+ apps, screenshot, clipboard |
| 🔊 | **Volume & Mute** | Voice-controlled system audio |
| 🔒 | **Screen Lock** | Lock Windows by just saying it |
| 🌐 | **Web Search** | Real-time DuckDuckGo search + news |
| 🌍 | **Browser Automation** | BUJJI can actually browse websites for you |
| 📧 | **Email** | Send Gmail with attachments |
| 💬 | **WhatsApp** | Send messages hands-free |
| ⏰ | **Reminders** | Set voice reminders |
| 📊 | **System Monitor** | Background CPU/RAM/battery alerts |
| 🖥️ | **Web Dashboard** | Chat UI + live stats at localhost:8000 |

---

## 🛠️ Tech Stack — Everything Free

```
Wake Word    →  Picovoice Porcupine   (offline, custom model)
LLM          →  Groq llama-3.3-70b    (free API)
Agent        →  LangGraph ReAct       (tool-calling agent)
Memory       →  ChromaDB              (local vector store)
Speech In    →  Google Speech API     (free)
Speech Out   →  pyttsx3               (offline TTS)
Browser      →  Playwright Chromium   (automation)
API          →  FastAPI               (REST server)
UI           →  Rich CLI + HTML       (dashboard)
```

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/Vaibhavsharma45/Bujji_AI.git
cd Bujji_AI
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 4. Add your API keys

```bash
copy .env.example .env
```

Open `.env` and fill in:

```env
GROQ_API_KEY=your_key_here        # → console.groq.com (free)
PICOVOICE_KEY=your_key_here       # → console.picovoice.ai (free)
EMAIL_ADDRESS=your@gmail.com
EMAIL_PASSWORD=xxxx_xxxx_xxxx     # Gmail App Password
```

### 5. (Optional) Custom Wake Word

1. Go to [console.picovoice.ai](https://console.picovoice.ai) → Wake Word
2. Train any phrase — e.g. `hey bujji` or `hey robo`
3. Platform → **Windows (x86_64, arm64)**
4. Download `.ppn` → rename to `hey_bujji.ppn` → place in project root

### 6. Run!
```bash
python main.py
```

---

## 🎮 How to Use

Pick a mode when BUJJI starts:

```
[w]  Wake word mode  →  Say "Hey Robo" then speak
[v]  Voice mode      →  Just speak anytime
[t]  Text mode       →  Type commands
```

### Example Commands

```bash
# 🖥️  Apps & System
"open youtube"              → Opens YouTube
"open vscode"               → Launches VS Code
"volume 70 karo"            → Sets volume to 70%
"mute karo"                 → Toggles mute
"screen lock karo"          → Locks screen
"screenshot lo"             → Takes screenshot

# 🌐  Search & Web
"search latest AI news"     → Web search results
"play Arijit Singh"         → YouTube auto-play

# 📋  Productivity  
"set reminder at 18:00 chai peeni hai"
"calculate 25% of 4500"
"convert 10 km to miles"
"time kya hai"

# 📧  Communication
"send email to x@y.com subject Hi body Hello"
"send whatsapp to +91XXXXXXXXXX message Done"

# 🧠  Memory
"clear memory"
"memory stats"

# 👋  Exit
"bye" / "exit" / "band kar"
```

---

## 🌐 Web Dashboard

Start the API + dashboard:

```bash
uvicorn api.server:app --reload
```

Open **[http://localhost:8000](http://localhost:8000)**

- Live CPU / RAM / Battery stats
- Chat with BUJJI from browser
- Activity log
- Quick action buttons

---

## 📁 Project Structure

```
Bujji_AI/
├── main.py                 # Entry point
├── brain.py                # AI agent + FRIDAY personality  
├── voice.py                # Speech in/out
├── wake.py                 # Wake word detection
├── memory.py               # Vector memory
├── config.py               # Settings
│
├── tools/                  # All BUJJI capabilities
│   ├── pc_control.py       # Apps, files, system
│   ├── self_assistance.py  # Volume, lock, keyboard
│   ├── search.py           # Web + news search
│   ├── email_tool.py       # Gmail
│   ├── reminder.py         # Reminders
│   ├── calculator.py       # Math + units
│   ├── emotion.py          # Voice emotion
│   ├── autonomous_agent.py # Browser automation
│   └── ...
│
├── api/server.py           # FastAPI REST
├── ui/dashboard.html       # Web UI
├── assets/screenshots/     # Demo images
├── hey_bujji.ppn           # Wake word model
└── .env                    # Your keys (not in git)
```

---

## 👤 Author

**Vaibhav Sharma**
- GitHub: [@Vaibhavsharma45](https://github.com/Vaibhavsharma45)

---

<div align="center">

*Built with ❤️ — Not just a project, it's a personal AI that actually works.*

</div>
