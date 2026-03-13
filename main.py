#!/usr/bin/env python3
"""
BUJJI v3 — Personal AI Assistant
Entry point. Supports wake word, voice, and text modes.
Run: python main.py
"""
import os
import sys
import time
import threading
from datetime import datetime

# ── Rich CLI ──────────────────────────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel   import Panel
    from rich.text    import Text
    from rich.rule    import Rule
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

    def _info(msg):    _con.print(f"  [dim]→[/dim] {msg}", highlight=False)
    def _ok(msg):      _con.print(f"  [green]✓[/green] {msg}", highlight=False)
    def _warn(msg):    _con.print(f"  [yellow]![/yellow] {msg}", highlight=False)
    def _you(msg):     _con.print(f"\n  [bold white]You:[/bold white] [white]{msg}[/white]")
    def _bujji(msg):   _con.print(f"  [bold cyan]BUJJI:[/bold cyan] [cyan]{msg}[/cyan]\n")
    def _divider():    _con.print(Rule(style="dim"))

except ImportError:
    def _banner():   print("\n===  BUJJI v3 — Personal AI Assistant  ===\n")
    def _info(msg):  print(f"  → {msg}")
    def _ok(msg):    print(f"  ✓ {msg}")
    def _warn(msg):  print(f"  ! {msg}")
    def _you(msg):   print(f"\n  You: {msg}")
    def _bujji(msg): print(f"  BUJJI: {msg}\n")
    def _divider():  print("  " + "─" * 44)

# ── Project imports ───────────────────────────────────────────────────────────
from voice  import speak, listen, listen_raw
from brain  import ask_jarvis, clear_history
from memory import clear_memory, memory_stats
from config import PICOVOICE_KEY, validate
from logger import get_logger

log = get_logger("main")

# ── Command cleaner ───────────────────────────────────────────────────────────
_FILLERS = ["hey jarvis", "jarvis", "hey bujji", "bujji", "okay bujji", "ok bujji",
            "arre bujji", "suno bujji", "bujji suno"]

def _clean(text: str) -> str:
    for f in _FILLERS:
        text = text.replace(f, "")
    return text.strip()

# ── Built-in commands (no LLM, instant) ───────────────────────────────────────
def _builtin(cmd: str) -> tuple[bool, str]:
    if any(k in cmd for k in ["clear memory", "memory clear", "memory delete", "memory bhool ja"]):
        return True, clear_memory()
    if any(k in cmd for k in ["memory stats", "memory count", "kitni memories"]):
        return True, memory_stats()
    if any(k in cmd for k in ["clear history", "history clear", "chat clear"]):
        return True, clear_history()
    if cmd in ("time", "what time", "current time", "time kya hai", "time batao"):
        return True, f"It's {datetime.now().strftime('%I:%M %p')}, sir."
    if cmd in ("date", "today", "aaj ki date", "date batao"):
        return True, f"Today is {datetime.now().strftime('%A, %d %B %Y')}, sir."
    if any(k in cmd for k in ["band kar", "shut down", "shutdown", "goodbye", "bye bujji", "bye", "exit", "quit"]):
        speak("Goodbye sir. BUJJI shutting down. Have a great day!")
        log.info("Shutdown command received")
        sys.exit(0)
    return False, ""

# ── Core process ──────────────────────────────────────────────────────────────
def _process(text: str, raw_audio: bytes = b"", audio_sr: int = 0):
    """Clean input, detect emotion, run built-ins or LLM."""
    text = _clean(text)
    if not text:
        return

    _you(text)
    log.info(f"Input: {text}")

    # Built-in fast path
    handled, resp = _builtin(text)
    if handled:
        _bujji(resp)
        speak(resp)
        return

    # Emotion detection from raw audio
    emotion = "neutral"
    if raw_audio:
        from tools.emotion import detect_emotion
        em = detect_emotion(raw_audio, audio_sr)
        emotion = em.get("emotion", "neutral")
        if emotion != "neutral":
            log.debug(f"Emotion: {emotion}")

    _info("Thinking…")
    response = ask_jarvis(text, emotion)
    _bujji(response)
    speak(response)

# ── Wake word mode ─────────────────────────────────────────────────────────────
def _on_wake():
    speak("Yes sir!")
    time.sleep(1.2)          # Wait for TTS to finish before microphone opens
    _info("Listening for your command…")
    raw, sr = listen_raw()   # capture audio for emotion too
    from voice import _recognizer
    import speech_recognition as sr_lib
    # decode text from same audio
    text = ""
    if raw:
        try:
            import speech_recognition as sr_lib
            audio = sr_lib.AudioData(raw, sr if sr else 16000, 2)
            text  = _recognizer.recognize_google(audio, language="en-IN").lower().strip()
        except Exception:
            pass
    if not text:
        speak("Suna nahi sir. Dobara Jarvis bolo.")
        return
    _process(text, raw, sr)

def run_wake_mode():
    if PICOVOICE_KEY == "YOUR_KEY_HERE":
        _warn("PICOVOICE_KEY not set → https://console.picovoice.ai (free)")
        _warn("Falling back to direct voice mode.")
        run_voice_mode()
        return
    from wake import start_wake_detection
    speak("BUJJI online in wake word mode. Say Jarvis to activate me.")
    _ok(f"Wake word mode — say 'Jarvis'")
    _divider()
    start_wake_detection(on_wake_callback=_on_wake)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        from wake import stop_wake_detection
        stop_wake_detection()
        speak("BUJJI shutting down. Goodbye sir.")

# ── Direct voice mode ─────────────────────────────────────────────────────────
def run_voice_mode():
    speak("Direct voice mode active. Speak your command.")
    _ok("Voice mode — speak anytime")
    _divider()
    while True:
        _info("Listening…")
        raw, sr_rate = listen_raw()
        from voice import _recognizer
        text = ""
        if raw:
            try:
                import speech_recognition as sr_lib
                audio = sr_lib.AudioData(raw, sr_rate if sr_rate else 16000, 2)
                text  = _recognizer.recognize_google(audio, language="en-IN").lower().strip()
            except Exception:
                pass
        if not text:
            continue
        _process(text, raw, sr_rate)

# ── Text mode ──────────────────────────────────────────────────────────────────
def run_text_mode():
    speak("Text mode active.")
    _ok("Text mode — type your command")
    _divider()
    while True:
        try:
            raw_input = input("  You: ").strip()
        except (KeyboardInterrupt, EOFError):
            speak("Goodbye sir.")
            break
        if not raw_input:
            continue
        _process(raw_input)

# ── Entry point ────────────────────────────────────────────────────────────────
def main():
    _banner()
    validate()
    print()
    speak("BUJJI online. Systems ready. How can I assist you, sir?")

    print("  Select mode:")
    print("    [w]  Wake word  — say 'Jarvis' to activate (requires Picovoice key)")
    print("    [v]  Voice      — always listening, speak directly")
    print("    [t]  Text       — type commands")
    print()

    while True:
        try:
            mode = input("  Mode: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)
        if mode in ("w", "v", "t"):
            break
        _warn("Enter w, v, or t")

    _divider()
    if mode == "w":
        run_wake_mode()
    elif mode == "v":
        run_voice_mode()
    else:
        run_text_mode()

if __name__ == "__main__":
    main()