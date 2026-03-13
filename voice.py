import subprocess, sys, os, time
import speech_recognition as sr
from config import TTS_RATE, TTS_VOLUME, STT_LANGUAGE, STT_TIMEOUT, STT_PHRASE_LIMIT
from logger import get_logger

log = get_logger("voice")

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
        if any(k in v.name.lower() for k in ['david','mark','george','male']):
            e.setProperty('voice', v.id)
            break
    e.say(text)
    e.runAndWait()
    e.stop()
except Exception:
    pass
"""

_tts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_tts_worker.py")
with open(_tts_path, "w", encoding="utf-8") as _f:
    _f.write(_TTS_SCRIPT)


def speak(text, rate=TTS_RATE, volume=TTS_VOLUME):
    if not text:
        return
    text = text.strip()
    log.info("TTS: " + text[:80])
    try:
        kwargs = {}
        if os.name == "nt":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        subprocess.run(
            [sys.executable, _tts_path, text, str(rate), str(volume)],
            timeout=45, stderr=subprocess.DEVNULL, **kwargs,
        )
    except Exception as e:
        log.error("TTS: " + str(e))


_recognizer = sr.Recognizer()
_recognizer.pause_threshold = 0.8
_recognizer.energy_threshold = 300
_recognizer.dynamic_energy_threshold = True


def listen(timeout=STT_TIMEOUT, phrase_limit=STT_PHRASE_LIMIT):
    try:
        with sr.Microphone() as src:
            _recognizer.adjust_for_ambient_noise(src, duration=0.2)
            audio = _recognizer.listen(src, timeout=timeout, phrase_time_limit=phrase_limit)
        text = _recognizer.recognize_google(audio, language=STT_LANGUAGE)
        log.info("STT: " + text)
        return text.lower().strip()
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        log.error("Speech API: " + str(e))
        return ""
    except KeyboardInterrupt:
        raise
    except Exception as e:
        log.error("Listen: " + str(e))
        return ""


def listen_and_transcribe():
    """Listen once, return (text, raw_bytes, sample_rate). CPU-friendly."""
    try:
        with sr.Microphone(sample_rate=16000) as src:
            _recognizer.adjust_for_ambient_noise(src, duration=0.2)
            audio = _recognizer.listen(
                src,
                timeout=STT_TIMEOUT,
                phrase_time_limit=STT_PHRASE_LIMIT,
            )
        raw  = audio.get_raw_data(convert_rate=16000, convert_width=2)
        text = _recognizer.recognize_google(audio, language=STT_LANGUAGE)
        log.info("STT: " + text)
        return text.lower().strip(), raw, 16000
    except sr.WaitTimeoutError:
        time.sleep(0.3)   # CPU relief on silence
        return "", b"", 0
    except sr.UnknownValueError:
        time.sleep(0.2)
        return "", b"", 0
    except sr.RequestError as e:
        log.error("Speech API: " + str(e))
        time.sleep(1.0)
        return "", b"", 0
    except KeyboardInterrupt:
        raise
    except Exception as e:
        log.error("Listen: " + str(e))
        time.sleep(0.5)
        return "", b"", 0
