import pyttsx3
import speech_recognition as sr

def speak(text: str):
    """Fresh engine har baar — Windows pe runAndWait crash fix"""
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)
        voices = engine.getProperty("voices")
        for v in voices:
            if "male" in v.name.lower() or "david" in v.name.lower() or "zira" in v.name.lower():
                engine.setProperty("voice", v.id)
                break
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[TTS Error]: {e}")

def listen(timeout: int = 5) -> str:
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8
    recognizer.energy_threshold = 300
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=12)
            text = recognizer.recognize_google(audio, language="en-IN")
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            print("[Error]: Speech service unreachable. Check internet.")
            return ""
        except Exception as e:
            print(f"[Listen Error]: {e}")
            return ""