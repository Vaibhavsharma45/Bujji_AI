"""
voice.py — TTS and STT
TTS runs pyttsx3 in a fresh subprocess every call.
This is the only reliable fix for 'run loop already started' on Windows threads.
STT uses Google Speech Recognition with Indian English tuning.
"""
import subprocess
import sys
import os
import time
import speech_recognition as sr
from config import TTS_RATE, TTS_VOLUME, STT_LANGUAGE, STT_TIMEOUT, STT_PHRASE_LIMIT
from logger import get_logger

log = get_logger("voice")

# ── TTS ────────────────────────────────────────────────────────────────────────

_TTS_SCRIPT = """
import pyttsx3, sys
text = sys.argv[1]
rate = int(sys.argv[2])
vol  = float(sys.argv[3])
try:
    e = pyttsx3.init()
    e.setProperty('rate', rate)
    e.setProperty('volume', vol)
    voices = e.getProperty('voices')
    for v in voices:
        if any(k in v.name.lower() for k in ['david', 'mark', 'george', 'male']):
            e.setProperty('voice', v.id)
            break
    e.say(text)
    e.runAndWait()
    e.stop()
except Exception as ex:
    pass
"""

_tts_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_tts_worker.py")
with open(_tts_script_path, "w", encoding="utf-8") as _f:
    _f.write(_TTS_SCRIPT)


def speak(text: str, rate: int = TTS_RATE, volume: float = TTS_VOLUME):
    """Speak text aloud using a subprocess-isolated pyttsx3 engine."""
    if not text:
        return
    text = text.strip()
    log.info(f"TTS → {text[:80]}")
    try:
        kwargs = {}
        if os.name == "nt":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        subprocess.run(
            [sys.executable, _tts_script_path, text, str(rate), str(volume)],
            timeout=45,
            stderr=subprocess.DEVNULL,
            **kwargs,
        )
    except subprocess.TimeoutExpired:
        log.warning("TTS timed out")
    except Exception as e:
        log.error(f"TTS error: {e}")


# ── STT ────────────────────────────────────────────────────────────────────────

_recognizer                 = sr.Recognizer()
_recognizer.pause_threshold = 0.8
_recognizer.energy_threshold= 300
_recognizer.dynamic_energy_threshold = True


def listen(timeout: int = STT_TIMEOUT, phrase_limit: int = STT_PHRASE_LIMIT) -> str:
    """
    Listen from microphone and return transcribed text (lowercase, stripped).
    Returns empty string on silence, noise, or error.
    """
    with sr.Microphone() as src:
        _recognizer.adjust_for_ambient_noise(src, duration=0.3)
        log.debug("Microphone open — listening")
        try:
            audio = _recognizer.listen(src, timeout=timeout, phrase_time_limit=phrase_limit)
            text  = _recognizer.recognize_google(audio, language=STT_LANGUAGE)
            log.info(f"STT → {text}")
            return text.lower().strip()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            log.error(f"Speech API unavailable: {e}")
            return ""
        except Exception as e:
            log.error(f"Listen error: {e}")
            return ""


def listen_raw() -> tuple[bytes, int]:
    """
    Return raw audio bytes + sample_rate for emotion analysis.
    Returns (b"", 0) on failure.
    """
    with sr.Microphone(sample_rate=16000) as src:
        _recognizer.adjust_for_ambient_noise(src, duration=0.2)
        try:
            audio = _recognizer.listen(src, timeout=STT_TIMEOUT, phrase_time_limit=STT_PHRASE_LIMIT)
            return audio.get_raw_data(convert_rate=16000, convert_width=2), 16000
        except Exception:
            return b"", 0