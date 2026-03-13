#!/usr/bin/env python3
"""BUJJI v3 — Personal AI Assistant. Run: python main.py"""
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
        art.append("\n██████╗ ██╗   ██╗     ██╗██╗\n", "bold cyan")
        art.append("██╔══██╗██║   ██║     ██║██║\n", "bold cyan")
        art.append("██████╔╝██║   ██║     ██║██║\n", "bold cyan")
        art.append("██╔══██╗██║   ██║██   ██║██║\n", "bold cyan")
        art.append("██████╔╝╚██████╔╝╚█████╔╝██║\n", "bold cyan")
        art.append("╚═════╝  ╚═════╝  ╚════╝ ╚═╝\n", "bold cyan")
        art.append(f"Personal AI Assistant  v3.0 — {datetime.now().strftime('%d %b %Y')}\n", "dim")
        _con.print(Panel(art, border_style="cyan", padding=(0, 4)))
    def _info(m):  _con.print(f"  [dim]→[/dim] {m}", highlight=False)
    def _ok(m):    _con.print(f"  [green]✓[/green] {m}", highlight=False)
    def _warn(m):  _con.print(f"  [yellow]![/yellow] {m}", highlight=False)
    def _you(m):   _con.print(f"\n  [bold white]You:[/bold white] [white]{m}[/white]")
    def _bujji(m): _con.print(f"  [bold cyan]BUJJI:[/bold cyan] [cyan]{m}[/cyan]\n")
    def _div():    _con.print(Rule(style="dim"))
except ImportError:
    def _banner():   print("\n=== BUJJI v3 ===\n")
    def _info(m):    print(f"  -> {m}")
    def _ok(m):      print(f"  OK {m}")
    def _warn(m):    print(f"  !  {m}")
    def _you(m):     print(f"\n  You: {m}")
    def _bujji(m):   print(f"  BUJJI: {m}\n")
    def _div():      print("  " + "-" * 44)

from voice  import speak, listen_and_transcribe
from brain  import ask_jarvis, clear_history
from memory import clear_memory, memory_stats
from config import PICOVOICE_KEY, validate
from logger import get_logger

log = get_logger("main")

_FILLERS = ["hey jarvis","jarvis","hey bujji","bujji","okay bujji","ok bujji",
            "arre bujji","suno bujji","hey google","ok google"]

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
    if cmd in ("time","what time","current time","time kya hai","time batao"):
        return True, f"It's {datetime.now().strftime('%I:%M %p')}, sir."
    if cmd in ("date","today","aaj ki date","date batao"):
        return True, f"Today is {datetime.now().strftime('%A, %d %B %Y')}, sir."
    if any(k in cmd for k in ["band kar","shut down","shutdown","goodbye","bye bujji","bye","exit","quit"]):
        speak("Goodbye sir. BUJJI shutting down.")
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
        _bujji(resp)
        speak(resp)
        return
    emotion = "neutral"
    if raw:
        try:
            from tools.emotion import detect_emotion
            emotion = detect_emotion(raw, sr_rate or 16000).get("emotion", "neutral")
        except Exception:
            pass
    _info("Thinking...")
    response = ask_jarvis(text, emotion)
    _bujji(response)
    speak(response)

def _on_wake():
    speak("Yes sir!")
    time.sleep(1.2)
    _info("Listening for command...")
    text, raw, sr_rate = listen_and_transcribe()
    if not text:
        speak("Suna nahi sir, dobara Jarvis bolo.")
        return
    _process(text, raw, sr_rate)

def run_wake_mode():
    if PICOVOICE_KEY == "YOUR_KEY_HERE":
        _warn("PICOVOICE_KEY not set. Falling back to voice mode.")
        run_voice_mode()
        return
    from wake import start_wake_detection
    speak("BUJJI online. Say Jarvis to activate.")
    _ok("Wake word mode — say 'Jarvis'")
    _div()
    start_wake_detection(on_wake_callback=_on_wake)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        from wake import stop_wake_detection
        stop_wake_detection()
        speak("BUJJI shutting down.")

def run_voice_mode():
    speak("Voice mode active.")
    _ok("Voice mode — speak anytime")
    _div()
    while True:
        _info("Listening...")
        try:
            text, raw, sr_rate = listen_and_transcribe()
        except KeyboardInterrupt:
            speak("Goodbye sir.")
            break
        if not text:
            continue
        _process(text, raw, sr_rate)

def run_text_mode():
    speak("Text mode active.")
    _ok("Text mode — type your command")
    _div()
    while True:
        try:
            raw_input = input("  You: ").strip()
        except (KeyboardInterrupt, EOFError):
            speak("Goodbye sir.")
            break
        if not raw_input:
            continue
        _process(raw_input)

def main():
    _banner()
    validate()
    print()
    speak("BUJJI online. How can I assist you, sir?")
    print("  Select mode:")
    print("    [w]  Wake word")
    print("    [v]  Voice")
    print("    [t]  Text")
    print()
    while True:
        try:
            mode = input("  Mode: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)
        if mode in ("w","v","t"):
            break
        _warn("Enter w, v, or t")
    _div()
    if mode == "w":
        run_wake_mode()
    elif mode == "v":
        run_voice_mode()
    else:
        run_text_mode()

if __name__ == "__main__":
    main()