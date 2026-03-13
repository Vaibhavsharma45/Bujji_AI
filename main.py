from voice import speak, listen
from brain import ask_jarvis
from config import WAKE_WORD

def run_jarvis():
    speak("BUJJI online. How can I assist you, sir?")
    print("\n" + "="*50)
    print("   BUJJI is active. Say 'bujji' to wake me.")
    print("   Type 'quit' to exit.")
    print("="*50 + "\n")

    # Mode ek baar select karo
    while True:
        mode = input("Mode select karo — [v]oice ya [t]ext: ").strip().lower()
        if mode in ["v", "t"]:
            break
        print("Sirf 'v' ya 't' daalo.")

    if mode == "v":
        speak("Voice mode active. Bujji bolo jab baat karni ho.")
        print("\n[Voice mode active — 'bujji' bol ke activate karo]\n")
    else:
        speak("Text mode active.")
        print("\n[Text mode active]\n")

    # Main loop — mode ab nahi poochenga
    while True:
        try:
            if mode == "v":
                print(f"Listening for 'bujji'...")
                trigger = listen(timeout=8)
                print(f"[Heard]: '{trigger}'")

                wake_variants = ["bujji", "buji", "buddy", "boozy", "boo ji", "boo gee"]
                detected = any(w in trigger.lower() for w in wake_variants)

                if not detected:
                    # Silent retry — koi message nahi, seedha listen karo
                    continue

                speak("Yes sir!")
                print("BUJJI: Yes sir!")

                user_input = listen(timeout=10)
                print(f"[Command]: '{user_input}'")

                if not user_input:
                    speak("Suna nahi. Dobara boliye.")
                    continue

            else:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ["quit", "exit", "bye"]:
                    speak("Goodbye sir. BUJJI shutting down.")
                    break

            if "clear memory" in user_input.lower():
                from memory import clear_memory
                result = clear_memory()
                speak(result)
                print(f"BUJJI: {result}")
                continue

            print("\nProcessing...\n")
            response = ask_jarvis(user_input)
            speak(response)
            print(f"BUJJI: {response}\n")

        except KeyboardInterrupt:
            speak("BUJJI shutting down. Goodbye sir.")
            break

if __name__ == "__main__":
    run_jarvis()