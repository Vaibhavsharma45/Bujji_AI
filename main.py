from voice import speak, listen
from brain import ask_jarvis
from config import WAKE_WORD

def run_jarvis():
    speak("BUJJI online. How can I assist you, sir?")
    print("\n" + "="*50)
    print("   BUJJI is active and ready!")
    print("   Type 'quit' to exit.")
    print("="*50 + "\n")

    # Mode ek baar select karo
    while True:
        mode = input("Mode select karo — [v]oice ya [t]ext: ").strip().lower()
        if mode in ["v", "t"]:
            break
        print("Sirf 'v' ya 't' daalo.")

    if mode == "v":
        speak("Voice mode active. Bol do kya karna hai.")
        print("\n[Voice mode — seedha bolo, koi wake word nahi!]\n")
    else:
        speak("Text mode active.")
        print("\n[Text mode active]\n")

    while True:
        try:
            if mode == "v":
                print("Listening... (bolo)")
                user_input = listen(timeout=6)

                if not user_input:
                    continue

                print(f"You: {user_input}")

                # Exit commands
                if any(w in user_input for w in ["band kar", "shut down", "goodbye", "bye bujji", "exit"]):
                    speak("Goodbye sir. BUJJI shutting down.")
                    break

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