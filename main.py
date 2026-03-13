from voice import speak, listen
from brain import ask_bujji
from config import WAKE_WORD

def run_bujji():
    speak("BUJJI online. How can I assist you, sir?")
    print("\n" + "="*50)
    print("   BUJJI is running. Say 'bujji' to wake me.")
    print("   Type 'quit' to exit.")
    print("="*50 + "\n")

    while True:
        try:
            mode = input("Mode — [v]oice or [t]ext? (default: text): ").strip().lower()

            if mode == "v":
                print(f"\nListening for wake word '{WAKE_WORD}'...")
                print("(Tip: bolne ke baad 1-2 sec ruko)")
                trigger = listen(timeout=8)

                # Debug: show what was heard
                print(f"[Debug] Suna: '{trigger}'")

                # Flexible wake word check
                trigger_clean = trigger.lower().strip()
                wake_variants = [WAKE_WORD, "bujji", "travis", "davis", "service", "jar vis"]
                detected = any(w in trigger_clean for w in wake_variants)

                if not detected:
                    print("Wake word detect nahi hua. Dobara try karo ya 't' press karo text mode ke liye.")
                    continue

                speak("Yes sir, I'm listening.")
                user_input = listen(timeout=10)
                print(f"[Debug] Command suna: '{user_input}'")

                if not user_input:
                    speak("I didn't catch that. Please try again.")
                    continue

            else:
                user_input = input("\nYou: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ["quit", "exit", "bye"]:
                    speak("Goodbye sir. BUJJI going offline.")
                    break

            if "clear memory" in user_input.lower():
                from memory import clear_memory
                result = clear_memory()
                speak(result)
                continue

            print("\nProcessing...\n")
            response = ask_bujji(user_input)
            speak(response)
            print()

        except KeyboardInterrupt:
            speak("BUJJI shutting down. Goodbye sir.")
            break

if __name__ == "__main__":
    run_bujji()