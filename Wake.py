import pvporcupine
import pyaudio
import struct
import threading
from voice import speak

# ─── CONFIG ──────────────────────────────────────────────────────
# Free key: https://console.picovoice.ai  (signup → AccessKey copy karo)
PICOVOICE_KEY = "KdA+Hptz+YxsFsqvTklFbrPtm4ndd/+k51BbeeaUAlLT5E7N17cozQ=="

# Built-in wake words (free): hey barista, hey google, alexa, computer,
# hey siri, jarvis, picovoice, porcupine, bumblebee, terminator, grapefruit
WAKE_WORD = "jarvis"  # "jarvis" closest to "bujji" feel — ya "hey siri" bhi try karo

# ─────────────────────────────────────────────────────────────────

_listening = False
_thread    = None
_callback  = None

def _listen_loop():
    global _listening

    try:
        porcupine = pvporcupine.create(
            access_key=PICOVOICE_KEY,
            keywords=[WAKE_WORD]
        )
    except pvporcupine.PorcupineInvalidArgumentError:
        print("[Wake] Invalid access key. Get free key: https://console.picovoice.ai")
        return
    except Exception as e:
        print(f"[Wake] Init failed: {e}")
        return

    pa     = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

    print(f"[Wake] Listening for '{WAKE_WORD}'...")

    try:
        while _listening:
            pcm   = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm   = struct.unpack_from("h" * porcupine.frame_length, pcm)
            index = porcupine.process(pcm)

            if index >= 0:
                print("[Wake] Wake word detected!")
                speak("Yes sir!")
                if _callback:
                    threading.Thread(target=_callback, daemon=True).start()
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

def start_wake_detection(on_wake_callback):
    """
    Background mein wake word sunna shuru karo.
    on_wake_callback: function jo wake word detect hone pe call ho.
    """
    global _listening, _thread, _callback
    _callback  = on_wake_callback
    _listening = True
    _thread    = threading.Thread(target=_listen_loop, daemon=True)
    _thread.start()

def stop_wake_detection():
    global _listening
    _listening = False
    print("[Wake] Stopped.")