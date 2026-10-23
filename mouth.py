"""
Speaks a reply out loud one sentence at a time, while the rest of it is still
streaming in. Make a new Mouth for each reply.

    mouth = Mouth(voice="Daniel", rate=220)
    mouth.add("Hello th")       # feed it text as it arrives...
    mouth.add("ere. How are")   # ...it starts saying "Hello there." right away
    mouth.add(" you?")
    mouth.finish()              # says the rest, then waits until it's done talking
"""

import queue
import re
import subprocess
import threading

# A sentence ends at . ! or ? followed by a space, or at a line break.
SENTENCE_END = re.compile(r"(?<=[.!?])\s+|\n+")


class Mouth:
    def __init__(self, voice, rate):
        self.voice = voice
        self.rate = rate
        self.unfinished = ""
        # A queue is a waiting line: the streaming loop drops finished
        # sentences in, and the talking thread takes them out in order.
        self.sentences = queue.Queue()
        self.thread = threading.Thread(target=self._talk, daemon=True)
        self.thread.start()

    def add(self, text):
        """Feed in streamed text. Every finished sentence goes off to be spoken."""
        self.unfinished += text
        *finished, self.unfinished = SENTENCE_END.split(self.unfinished)
        for sentence in finished:
            self._queue(sentence)

    def finish(self):
        """Say whatever is left, then wait until Jarvis stops talking."""
        self._queue(self.unfinished)
        self.unfinished = ""
        self.sentences.put(None)  # None means "that's everything"
        self.thread.join()

    def _queue(self, sentence):
        if sentence.strip():
            self.sentences.put(sentence.strip())

    def _talk(self):
        while True:
            sentence = self.sentences.get()
            if sentence is None:
                return
            subprocess.run(["say", "-v", self.voice, "-r", str(self.rate), sentence])
