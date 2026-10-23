"""
A Claude-style "thinking" spinner: a spinning star and a silly word that show
while Jarvis waits for the model's first word.

    spinner = Spinner()
    spinner.start()
    ...  # slow stuff
    spinner.stop()
"""

import random
import threading
import time

THINKING_WORDS = [
    "Tomfoolering", "Ovulating", "Pondering", "Noodling", "Percolating",
    "Cogitating", "Bamboozling", "Ruminating", "Conjuring", "Schlepping",
    "Finagling", "Discombobulating", "Moseying", "Marinating", "Galumphing",
    "Flibbertigibbeting", "Hullaballooing", "Befuddling", "Shenaniganing",
]

FRAMES = "·✢✳✶✻✽✻✶✳✢"


class Spinner:
    def __init__(self):
        self.word = random.choice(THINKING_WORDS)
        self.stopped = threading.Event()
        self.thread = threading.Thread(target=self._spin, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        """Stop spinning and wipe the line. Safe to call more than once."""
        if self.stopped.is_set():
            return
        self.stopped.set()
        self.thread.join()
        print("\r\033[K", end="", flush=True)

    def _spin(self):
        start = time.time()
        frame = 0
        while not self.stopped.is_set():
            star = FRAMES[frame % len(FRAMES)]
            seconds = int(time.time() - start)
            print(f"\r{star} {self.word}… ({seconds}s)", end="", flush=True)
            frame += 1
            time.sleep(0.12)
