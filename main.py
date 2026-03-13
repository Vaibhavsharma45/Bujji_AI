import time
from voice import speak, listen
from brain import ask_jarvis
from config import WAKE_WORD

def run_jarvis():
    speak("JARVIS online. How can I assist you, sir?")
    print("\n" + "="*50)
    print("   JARVIS is running. Say 'jarvis' to wake me.")
    print("   Type 'quit' to exit.")
    print("="*50 + "\n")

    while True:
        try:
            mode = input("Mode — [v]oice or [t]ext? (default: text): ").strip().lower()

            if mode == "v":
                print(f"\nListening for wake word '{WAKE_WORD}'...")
                trigger = listen(timeout=8)
                if WAKE_WORD not in trigger:
                    print("Wake word not detected. Try again.")
                    continue
                speak("Yes sir, I'm listening.")
                user_input = listen(timeout=10)
                if not user_input:
                    speak("I didn't catch that. Please try again.")
                    continue
            else:
                user_input = input("\nYou: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ["quit", "exit", "bye"]:
                    speak("Goodbye sir. JARVIS going offline.")
                    break

            if "clear memory" in user_input.lower():
                from memory import clear_memory
                result = clear_memory()
                speak(result)
                continue

            print("\nProcessing...\n")
            response = ask_jarvis(user_input)
            speak(response)
            print()

        except KeyboardInterrupt:
            speak("JARVIS shutting down. Goodbye sir.")
            break

if __name__ == "__main__":
    run_jarvis()