import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
for v in voices:
    if "male" in v.name.lower() or "david" in v.name.lower():
        engine.setProperty("voice", v.id)
        break

def speak(text: str):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def listen(timeout: int = 5) -> str:
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language="en-IN")
            print(f"You: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Sorry, I couldn't reach the speech service. Check your internet.")
            return ""