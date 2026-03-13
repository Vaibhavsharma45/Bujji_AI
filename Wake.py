import pvporcupine
import pyaudio
import struct
import threading
import time

PICOVOICE_KEY = "YOUR_ACCESS_KEY_HERE"
WAKE_WORD     = "jarvis"

_listening  = False
_thread     = None
_callback   = None
_cooldown   = False  # Duplicate detection rok ne ke liye

def _listen_loop():
    global _listening, _cooldown

    try:
        porcupine = pvporcupine.create(
            access_key=PICOVOICE_KEY,
            keywords=[WAKE_WORD]
        )
    except pvporcupine.PorcupineInvalidArgumentError:
        print("[Wake] Invalid key. Free key: https://console.picovoice.ai")
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

    print(f"[Wake] Ready — '{WAKE_WORD}' bolo...")

    try:
        while _listening:
            pcm   = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm   = struct.unpack_from("h" * porcupine.frame_length, pcm)
            index = porcupine.process(pcm)

            if index >= 0 and not _cooldown:
                _cooldown = True
                print("[Wake] Detected!")
                threading.Thread(target=_callback, daemon=True).start()
                time.sleep(3)  # 3 sec cooldown — double trigger nahi hoga
                _cooldown = False
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

def start_wake_detection(on_wake_callback):
    global _listening, _thread, _callback
    _callback  = on_wake_callback
    _listening = True
    _thread    = threading.Thread(target=_listen_loop, daemon=True)
    _thread.start()

def stop_wake_detection():
    global _listening
    _listening = False