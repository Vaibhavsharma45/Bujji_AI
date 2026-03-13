import pvporcupine
import pyaudio
import struct
import threading
import time

PICOVOICE_KEY = "KdA+Hptz+YxsFsqvTklFbrPtm4ndd/+k51BbeeaUAlLT5E7N17cozQ=="
WAKE_WORD     = "Hey Bujji"

_listening  = False
_thread     = None
_callback   = None
_lock       = threading.Lock()
_processing = False  # Command process ho raha hai ya nahi

def _listen_loop():
    global _listening, _processing

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

            if index >= 0:
                with _lock:
                    if _processing:
                        continue  # Already processing — ignore
                    _processing = True

                print("[Wake] Detected!")
                threading.Thread(target=_run_callback, daemon=True).start()
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

def _run_callback():
    global _processing
    try:
        if _callback:
            _callback()
    finally:
        time.sleep(2)
        _processing = False  # Done — ab dobara sun sakte hain

def start_wake_detection(on_wake_callback):
    global _listening, _thread, _callback
    _callback  = on_wake_callback
    _listening = True
    _thread    = threading.Thread(target=_listen_loop, daemon=True)
    _thread.start()

def stop_wake_detection():
    global _listening
    _listening = False