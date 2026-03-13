#!/usr/bin/env python3
"""BUJJI v4 — FRIDAY Edition. Run: python main.py"""
import os, sys, time, threading
from datetime import datetime

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.rule import Rule
    _con = Console()
    def _banner():
        art = Text(justify="center")
        art.append("\n███████╗██████╗ ██╗██████╗  █████╗ ██╗   ██╗\n", "bold magenta")
        art.append("██╔════╝██╔══██╗██║██╔══██╗██╔══██╗╚██╗ ██╔╝\n", "bold magenta")
        art.append("█████╗  ██████╔╝██║██║  ██║███████║ ╚████╔╝ \n", "bold magenta")
        art.append("██╔══╝  ██╔══██╗██║██║  ██║██╔══██║  ╚██╔╝  \n", "bold magenta")
        art.append("██║     ██║  ██║██║██████╔╝██║  ██║   ██║   \n", "bold magenta")
        art.append("╚═╝     ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   \n", "bold magenta")
        art.append(f"BUJJI — FRIDAY Edition  v4.0 — {datetime.now().strftime('%d %b %Y')}\n", "dim")
        _con.print(Panel(art, border_style="magenta", padding=(0, 2)))
    def _info(m):  _con.print(f"  [dim]→[/dim] {m}", highlight=False)
    def _ok(m):    _con.print(f"  [green]✓[/green] {m}", highlight=False)
    def _warn(m):  _con.print(f"  [yellow]![/yellow] {m}", highlight=False)
    def _you(m):   _con.print(f"\n  [bold white]You:[/bold white] [white]{m}[/white]")
    def _fri(m):   _con.print(f"  [bold magenta]FRIDAY:[/bold magenta] [magenta]{m}[/magenta]\n")
    def _div():    _con.print(Rule(style="dim"))
except ImportError:
    def _banner():   print("\n=== BUJJI v4 FRIDAY Edition ===\n")
    def _info(m):    print(f"  -> {m}")
    def _ok(m):      print(f"  OK {m}")
    def _warn(m):    print(f"  !  {m}")
    def _you(m):     print(f"\n  You: {m}")
    def _fri(m):     print(f"  FRIDAY: {m}\n")
    def _div():      print("  " + "-" * 50)

from voice  import speak, listen_and_transcribe
from brain  import ask_jarvis, clear_history
from memory import clear_memory, memory_stats
from config import PICOVOICE_KEY, validate
from logger import get_logger

log = get_logger("main")

_FILLERS = ["hey jarvis","jarvis","hey bujji","bujji","hey friday","friday",
            "okay friday","ok friday","hey google","ok google","arre bujji"]

def _clean(t):
    for f in _FILLERS:
        t = t.replace(f, "")
    return t.strip()

def _builtin(cmd):
    if any(k in cmd for k in ["clear memory","memory clear","memory delete"]):
        return True, clear_memory()
    if any(k in cmd for k in ["memory stats","kitni memories"]):
        return True, memory_stats()
    if any(k in cmd for k in ["clear history","chat clear"]):
        return True, clear_history()
    if cmd in ("time","what time","time kya hai","time batao","abhi kitna baj raha hai"):
        return True, f"Bhaiya, abhi {datetime.now().strftime('%I:%M %p')} baj rahe hain!"
    if cmd in ("date","today","aaj ki date","date batao"):
        return True, f"Aaj {datetime.now().strftime('%A, %d %B %Y')} hai bhaiya."
    if any(k in cmd for k in ["band kar","shut down","shutdown","goodbye","bye","exit","quit","soja"]):
        speak("Theek hai bhaiya, main so raha hoon. Bye bye!")
        sys.exit(0)
    return False, ""

def _process(text, raw=b"", sr_rate=0):
    text = _clean(text)
    if not text:
        return
    _you(text)
    log.info(f"Input: {text}")
    handled, resp = _builtin(text)
    if handled:
        _fri(resp)
        speak(resp)
        return
    emotion = "neutral"
    if raw:
        try:
            from tools.emotion import detect_emotion
            emotion = detect_emotion(raw, sr_rate or 16000).get("emotion", "neutral")
        except Exception:
            pass
    _info("Soch raha hoon...")
    response = ask_jarvis(text, emotion)
    _fri(response)
    speak(response)

def _on_wake():
    speak("Haan bhaiya, bolo!")
    time.sleep(1.0)
    _info("Command sun raha hoon...")
    text, raw, sr_rate = listen_and_transcribe()
    if not text:
        speak("Suna nahi bhaiya, dobara Jarvis bolo.")
        return
    _process(text, raw, sr_rate)

def run_wake_mode():
    if PICOVOICE_KEY == "YOUR_KEY_HERE":
        _warn("PICOVOICE_KEY set nahi hai. Voice mode pe aa raha hoon.")
        run_voice_mode()
        return
    from wake import start_wake_detection
    speak("FRIDAY online bhaiya. Jarvis bolo toh main sun lunga!")
    _ok("Wake word mode — say 'Jarvis'")
    _div()
    start_wake_detection(on_wake_callback=_on_wake)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        from wake import stop_wake_detection
        stop_wake_detection()
        speak("Theek hai bhaiya, so raha hoon. Bye!")

def run_voice_mode():
    speak("Voice mode active bhaiya. Bolo kya karna hai!")
    _ok("Voice mode — speak anytime")
    _div()
    while True:
        _info("Sun raha hoon...")
        try:
            text, raw, sr_rate = listen_and_transcribe()
        except KeyboardInterrupt:
            speak("Bye bhaiya!")
            break
        if not text:
            continue
        _process(text, raw, sr_rate)

def run_text_mode():
    speak("Text mode bhaiya. Type karo!")
    _ok("Text mode — type your command")
    _div()
    while True:
        try:
            raw_input = input("  You: ").strip()
        except (KeyboardInterrupt, EOFError):
            speak("Bye bhaiya!")
            break
        if not raw_input:
            continue
        _process(raw_input)

def main():
    _banner()
    validate()
    print()
    speak("FRIDAY online! Bolo bhaiya, kya karna hai aaj?")
    print("  Mode select karo:")
    print("    [w]  Wake word  (Jarvis bolo)")
    print("    [v]  Voice      (seedha bolo)")
    print("    [t]  Text       (type karo)")
    print()
    while True:
        try:
            mode = input("  Mode: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)
        if mode in ("w","v","t"):
            break
        _warn("w, v, ya t daalo bhaiya")
    _div()
    if mode == "w":
        run_wake_mode()
    elif mode == "v":
        run_voice_mode()
    else:
        run_text_mode()

if __name__ == "__main__":
    main()