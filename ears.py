"""
Records your voice from the Mac's microphone.

    audio = record()      # starts listening, press Enter to stop
    if is_silent(audio):  # nothing worth sending to Whisper
        ...
"""

import numpy as np
import sounddevice as sd

# Sound is just a long list of numbers: how far the microphone is pushed at
# each instant. Whisper wants 16,000 of them for every second of sound.
SAMPLE_RATE = 16000


def record():
    """Record until you press Enter. Returns the sound as one long list of numbers."""
    pieces = []

    # sounddevice calls this every few milliseconds with the newest bit of
    # sound, a lot like the chunks you get when streaming from Ollama.
    def save_piece(indata, frames, time, status):
        pieces.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", callback=save_piece):
        input("🎤 Listening... press Enter when you're done.")

    if not pieces:
        return np.zeros(0, dtype=np.float32)
    return np.concatenate(pieces).flatten()


def is_silent(audio):
    """True if the recording is too short or too quiet to be speech."""
    if len(audio) < SAMPLE_RATE * 0.3:
        return True
    # Average loudness (called RMS). The single loudest moment isn't enough:
    # one random crackle of room noise would count as "speech".
    loudness = np.sqrt(np.mean(audio**2))
    return loudness < 0.005
