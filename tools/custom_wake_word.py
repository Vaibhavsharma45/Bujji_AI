"""
tools/custom_wake_word.py — Custom Wake Word Training
Uses Picovoice Porcupine with a custom "Hey BUJJI" keyword model.
Falls back to "jarvis" built-in if custom model not available.
"""
import os, threading, time, struct
from logger import get_logger

log = get_logger("wake")

_listening  = False
_thread     = None
_callback   = None
_processing = False
_lock       = threading.Lock()

# Path where user puts their custom .ppn model file
CUSTOM_MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "hey_bujji.ppn"
)


def _listen_loop():
    global _listening, _processing
    import pvporcupine, pyaudio

    access_key = os.getenv("PICOVOICE_KEY", "")

    try:
        # Try custom "Hey BUJJI" model first
        if os.path.exists(CUSTOM_MODEL_PATH):
            porcupine = pvporcupine.create(
                access_key=access_key,
                keyword_paths=[CUSTOM_MODEL_PATH],
            )
            log.info("Custom wake word 'Hey BUJJI' loaded!")
            print("  [Wake] Custom 'Hey BUJJI' model loaded!")
        else:
            # Fallback to built-in jarvis
            porcupine = pvporcupine.create(
                access_key=access_key,
                keywords=["jarvis"],
            )
            log.info("Using built-in 'Jarvis' wake word (no hey_bujji.ppn found)")
            print("  [Wake] Using 'Jarvis' wake word.")
            print("  [Wake] Custom 'Hey BUJJI' ke liye: hey_bujji.ppn project folder mein daalo")
            print("  [Wake] Download: https://console.picovoice.ai -> Wake Word -> Create 'hey bujji'")

    except pvporcupine.PorcupineActivationError:
        print("  [Wake] Invalid Picovoice key!")
        return
    except Exception as e:
        print(f"  [Wake] Init failed: {e}")
        return

    pa     = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

    try:
        while _listening:
            pcm   = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm   = struct.unpack_from("h" * porcupine.frame_length, pcm)
            index = porcupine.process(pcm)
            if index >= 0:
                with _lock:
                    if _processing:
                        continue
                    _processing = True
                log.info("Wake word detected!")
                threading.Thread(target=_fire, daemon=True).start()
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()


def _fire():
    global _processing
    try:
        if _callback:
            _callback()
    finally:
        time.sleep(2.5)
        _processing = False


def start_wake_detection(on_wake_callback):
    global _listening, _thread, _callback
    _callback  = on_wake_callback
    _listening = True
    _thread    = threading.Thread(target=_listen_loop, daemon=True)
    _thread.start()


def stop_wake_detection():
    global _listening
    _listening = False