import threading
from voice import speak, listen
from brain import ask_jarvis

USE_WAKE_WORD = False  # True karo jab pvporcupine setup ho jaaye

def handle_command():
    """Wake word detect hone ke baad command suno aur process karo."""
    user_input = listen(timeout=8)
    if not user_input:
        speak("Suna nahi, dobara boliye.")
        return
    print(f"You: {user_input}")

    if any(w in user_input for w in ["band kar", "shut down", "bye bujji"]):
        speak("Goodbye sir. BUJJI shutting down.")
        return

    if "clear memory" in user_input:
        from memory import clear_memory
        speak(clear_memory())
        return

    print("Processing...")
    response = ask_jarvis(user_input)
    speak(response)
    print(f"BUJJI: {response}\n")

def run_voice_mode_with_wake_word():
    from wake import start_wake_detection, stop_wake_detection, PICOVOICE_KEY
    if PICOVOICE_KEY == "YOUR_ACCESS_KEY_HERE":
        print("[!] Pehle wake.py mein PICOVOICE_KEY set karo.")
        print("    Free key: https://console.picovoice.ai")
        return False

    speak("BUJJI online. Wake word mode active.")
    print("\n[Wake word mode — 'Jarvis' bolo activate karne ke liye]\n")
    start_wake_detection(on_wake_callback=handle_command)
    return True

def run_direct_voice_mode():
    speak("Voice mode active. Seedha bolo.")
    print("\n[Voice mode — seedha bolo]\n")
    while True:
        print("Listening...")
        user_input = listen(timeout=6)
        if not user_input:
            continue
        print(f"You: {user_input}")

        if any(w in user_input for w in ["band kar", "shut down", "bye bujji", "exit"]):
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
        started = run_voice_mode_with_wake_word()
        if started:
            try:
                threading.Event().wait()  # Keep alive
            except KeyboardInterrupt:
                from wake import stop_wake_detection
                stop_wake_detection()
                speak("BUJJI shutting down.")
    elif mode == "v":
        run_direct_voice_mode()
    else:
        run_text_mode()

if __name__ == "__main__":
    run_bujji()