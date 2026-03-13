import threading
import time
from voice import speak, listen
from brain import ask_jarvis

def clean_command(text: str) -> str:
    for filler in ["hey jarvis", "jarvis", "hey bujji", "bujji", "okay bujji"]:
        text = text.replace(filler, "").strip()
    return text.strip()

def handle_command():
    speak("Yes sir!")
    time.sleep(1.5)  # TTS khatam hone ka wait karo
    
    print("Listening for command...")
    user_input = listen(timeout=8)

    if not user_input:
        speak("Suna nahi, dobara Jarvis bolo.")
        return

    user_input = clean_command(user_input)
    if not user_input:
        speak("Command samajh nahi aayi.")
        return

    print(f"You: {user_input}")

    if any(w in user_input for w in ["band kar", "shut down", "bye", "exit"]):
        speak("Goodbye sir.")
        return

    if "clear memory" in user_input:
        from memory import clear_memory
        speak(clear_memory())
        return

    print("Processing...")
    response = ask_jarvis(user_input)
    speak(response)
    print(f"BUJJI: {response}\n")

def run_wake_mode():
    from wake import start_wake_detection, PICOVOICE_KEY
    if PICOVOICE_KEY == "YOUR_ACCESS_KEY_HERE":
        print("[!] wake.py mein PICOVOICE_KEY set karo.")
        print("    Free key: https://console.picovoice.ai")
        return
    speak("BUJJI online. Wake word mode active.")
    print("\n[Wake word mode — 'Jarvis' bolo]\n")
    start_wake_detection(on_wake_callback=handle_command)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        from wake import stop_wake_detection
        stop_wake_detection()
        speak("BUJJI shutting down.")

def run_voice_mode():
    speak("Voice mode active.")
    print("\n[Voice mode — seedha bolo]\n")
    while True:
        print("Listening...")
        user_input = listen(timeout=6)
        if not user_input:
            continue
        user_input = clean_command(user_input)
        if not user_input:
            continue
        print(f"You: {user_input}")
        if any(w in user_input for w in ["band kar", "shut down", "bye", "exit"]):
            speak("Goodbye sir.")
            break
        if "clear memory" in user_input:
            from memory import clear_memory
            speak(clear_memory())
            continue
        print("Processing...")
        response = ask_jarvis(user_input)
        speak(response)
        print(f"BUJJI: {response}\n")

def run_text_mode():
    speak("Text mode active.")
    print("\n[Text mode]\n")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["quit", "exit", "bye"]:
            speak("Goodbye sir.")
            break
        if "clear memory" in user_input.lower():
            from memory import clear_memory
            speak(clear_memory())
            continue
        print("Processing...")
        response = ask_jarvis(user_input)
        speak(response)
        print(f"BUJJI: {response}\n")

def run_bujji():
    speak("BUJJI online. How can I assist you, sir?")
    print("\n" + "="*50)
    print("   BUJJI v2 is active!")
    print("="*50 + "\n")

    while True:
        mode = input("Mode — [v]oice / [w]ake word / [t]ext: ").strip().lower()
        if mode in ["v", "w", "t"]:
            break

    if mode == "w":
        run_wake_mode()
    elif mode == "v":
        run_voice_mode()
    else:
        run_text_mode()

if __name__ == "__main__":
    run_bujji()