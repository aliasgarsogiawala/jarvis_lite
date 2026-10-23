"""
Level 2: Ears and voice. Talk to Jarvis and it talks back.

Run it:  uv run level2_voice.py
Quit:    say "bye"
"""

import subprocess
from mouth import Mouth
import mlx_whisper

from ears import is_silent, record
from level1_brain import MODEL, SYSTEM_PROMPT, ask, wants_to_quit

WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"
VOICE = "Samantha"
RATE=220

# STEP 3: Jarvis's replies are spoken now. Add a rule so it talks like a
# person instead of writing like a document.
VOICE_PROMPT = VOICE_PROMPT = SYSTEM_PROMPT + """

Your replies are spoken aloud, so talk like a person: plain sentences, no markdown, lists or emojis. Also make mean comments"""


def hear(audio):
    """Turn recorded sound into text with Whisper."""
    result = mlx_whisper.transcribe(audio, path_or_hf_repo=WHISPER_MODEL)
    return result["text"].strip()

def speak(text):
    """Say text out loud, highlighting each word as it's spoken."""
    mouth = Mouth(VOICE, RATE)
    mouth.add(text)
    mouth.finish()
    


def main():
    print(f"Jarvis is listening, running {MODEL}. Say 'bye' to quit.\n")
    history = [{"role": "system", "content": VOICE_PROMPT}]

    while True:
        audio = record()
        if is_silent(audio):
            print("(didn't hear anything)")
            continue
        text = hear(audio)
        print(f"You: {text}")
        if wants_to_quit(text):
            print("Jarvis:")
            speak("See you later sir!")
            break
        history.append({"role": "user", "content": text})
        print("Jarvis:")
        mouth = Mouth(VOICE, RATE)
        reply = ask(history, on_piece=mouth.add, show=False)
        mouth.finish()
        history.append({"role": "assistant", "content": reply})



if __name__ == "__main__":
    main()
