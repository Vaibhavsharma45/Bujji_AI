import speech_recognition as sr
import subprocess
import sys
import os

def speak(text: str):
    """
    Windows pe pyttsx3 thread crash fix.
    subprocess mein alag Python process chalata hai — 100% reliable.
    """
    print(f"BUJJI: {text}")
    try:
        script = f"""
import pyttsx3
e = pyttsx3.init()
e.setProperty('rate', 165)
e.setProperty('volume', 1.0)
voices = e.getProperty('voices')
for v in voices:
    if 'david' in v.name.lower() or 'male' in v.name.lower():
        e.setProperty('voice', v.id)
        break
e.say({repr(text)})
e.runAndWait()
"""
        subprocess.run(
            [sys.executable, "-c", script],
            timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        )
    except subprocess.TimeoutExpired:
        pass
    except Exception as e:
        print(f"[TTS Error]: {e}")

def listen(timeout: int = 6) -> str:
    recognizer = sr.Recognizer()
    recognizer.pause_threshold  = 0.8
    recognizer.energy_threshold = 300

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=12)
            text  = recognizer.recognize_google(audio, language="en-IN")
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            print("[Error]: Speech service unreachable.")
            return ""
        except Exception as e:
            print(f"[Listen Error]: {e}")
            return ""