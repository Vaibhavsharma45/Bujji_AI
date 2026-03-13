"""
tools/emotion.py — Voice Emotion Detection
Pure signal-processing approach using librosa features.
No ML model needed — fast, offline, zero-cost.
Detects: neutral, happy, sad, angry, stressed
"""
import numpy as np
from logger import get_logger

log = get_logger("tool.emotion")

EMOTIONS = {
    "angry":   "User sounds frustrated. Be calm, brief, solution-first.",
    "sad":     "User sounds low energy or sad. Be warm, supportive, and gentle.",
    "happy":   "User sounds positive. Match the energy, be enthusiastic.",
    "stressed":"User sounds rushed or stressed. Give short, direct answers only.",
    "neutral": "",
}


def detect_emotion(audio_bytes: bytes, sample_rate: int = 16000) -> dict:
    """
    Analyse raw audio bytes and return emotion + tone hint.
    Returns dict with 'emotion', 'mood', 'energy', 'pitch', 'tone_hint'.
    Falls back to neutral on any error or missing library.
    """
    result = {"emotion": "neutral", "mood": "calm", "energy": 0.0, "pitch": 0.0, "tone_hint": ""}

    if not audio_bytes:
        return result

    try:
        import librosa
        y = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        if len(y) < sample_rate * 0.5:   # less than 0.5s — not enough data
            return result

        # Feature extraction
        rms = float(np.sqrt(np.mean(y ** 2)))
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))

        pitches, mags = librosa.piptrack(y=y, sr=sample_rate)
        pitch_vals = pitches[mags > np.median(mags)]
        pitch = float(np.mean(pitch_vals)) if len(pitch_vals) > 0 else 0.0

        spec_cen = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sample_rate)))

        # Heuristic classifier
        if rms > 0.08 and pitch > 220 and zcr > 0.12:
            emotion, mood = "angry",   "frustrated"
        elif rms > 0.055 and pitch > 195 and spec_cen > 2000:
            emotion, mood = "happy",   "positive"
        elif rms < 0.018 and pitch < 135:
            emotion, mood = "sad",     "low energy"
        elif zcr > 0.14 and rms > 0.045:
            emotion, mood = "stressed","rushed"
        else:
            emotion, mood = "neutral", "calm"

        log.debug(f"Emotion → {emotion} | rms={rms:.3f} pitch={pitch:.0f} zcr={zcr:.3f}")
        return {
            "emotion":   emotion,
            "mood":      mood,
            "energy":    round(rms, 3),
            "pitch":     round(pitch, 1),
            "tone_hint": EMOTIONS[emotion],
        }

    except ImportError:
        log.debug("librosa not installed — emotion detection disabled")
        return result
    except Exception as e:
        log.warning(f"Emotion detection error: {e}")
        return result


def emotion_tone_hint(emotion: str) -> str:
    return EMOTIONS.get(emotion, "")