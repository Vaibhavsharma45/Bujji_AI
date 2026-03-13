"""
wake.py — Offline wake word detection using pvporcupine.
Uses a threading lock to prevent double-triggering.
"""
import pvporcupine
import pyaudio
import struct
import threading
import time
from config import PICOVOICE_KEY, WAKE_WORD, WAKE_COOLDOWN
from logger import get_logger

log = get_logger("wake")

_listening:  bool  = False
_thread:     threading.Thread | None = None
_callback          = None
_processing: bool  = False
_lock              = threading.Lock()


def _listen_loop():
    global _listening, _processing

    try:
        porcupine = pvporcupine.create(access_key=PICOVOICE_KEY, keywords=[WAKE_WORD])
        log.info(f"Wake detection ready — keyword: '{WAKE_WORD}'")
        print(f"  [Wake] Listening for '{WAKE_WORD}'…")
    except pvporcupine.PorcupineActivationError:
        print("  [Wake] Invalid Picovoice key → https://console.picovoice.ai")
        log.error("Invalid Picovoice key")
        return
    except pvporcupine.PorcupineInvalidArgumentError as e:
        print(f"  [Wake] Keyword error: {e}")
        log.error(f"Keyword error: {e}")
        return
    except Exception as e:
        print(f"  [Wake] Init failed: {e}")
        log.error(f"Init failed: {e}")
        return

    pa     = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate, channels=1,
        format=pyaudio.paInt16, input=True,
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
                log.info("Wake word detected")
                threading.Thread(target=_fire_callback, daemon=True).start()
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
        log.info("Wake detection stopped")


def _fire_callback():
    global _processing
    try:
        if _callback:
            _callback()
    finally:
        time.sleep(WAKE_COOLDOWN)
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