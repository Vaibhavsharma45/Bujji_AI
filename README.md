# JARVIS - AI Personal Assistant

Your own Iron Man JARVIS — voice + web search + PC control + WhatsApp + email, completely free.

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API keys
```bash
cp .env.example .env
# Edit .env and add your keys
```

**Get free Groq API key:** https://console.groq.com  
**Gmail App Password:** https://myaccount.google.com/apppasswords

### 3. Run JARVIS
```bash
python main.py
```

## Usage

| Command | What happens |
|---|---|
| "Search for latest AI news" | Web search via DuckDuckGo |
| "Open Chrome" | Launches Chrome browser |
| "Take a screenshot" | Saves screenshot to home folder |
| "Send email to X about Y" | Sends email via Gmail |
| "WhatsApp John: meeting at 5" | Sends WhatsApp message |
| "What files are in downloads?" | Lists directory contents |
| "Clear memory" | Wipes conversation history |

## Tech Stack (100% Free)

- **LLM**: Groq + Llama 3 70B (free tier)
- **Voice**: SpeechRecognition + pyttsx3 (offline)
- **Search**: DuckDuckGo (no API key needed)
- **Memory**: ChromaDB (local)
- **Agent**: LangChain ReAct agent
- **Email**: smtplib (built-in Python)
- **WhatsApp**: pywhatkit

## Project Structure

```
jarvis/
├── main.py          # Entry point — run this
├── brain.py         # LangChain agent + Groq LLM
├── voice.py         # Speech input/output
├── memory.py        # ChromaDB conversation memory
├── config.py        # Settings and API keys
├── tools/
│   ├── search.py    # DuckDuckGo web search
│   ├── pc_control.py # App/file/screenshot control
│   ├── email_tool.py # Gmail sender
│   └── whatsapp.py  # WhatsApp via pywhatkit
└── requirements.txt
```