"""
Checks how well wants_to_quit() spots goodbyes. Rerun it whenever you change
QUIT_CHECK_PROMPT or QUIT_MODEL in level1_brain.py.

Run it:            uv run test_quit.py
Try another model: uv run test_quit.py llama3.1:8b
"""

import sys
import time

import level1_brain
from level1_brain import wants_to_quit

# Each line is (what the user types, should Jarvis quit?).
# Don't copy these sentences into the prompt's examples: the score would go up
# without the detector getting any better. That's overfitting.
CASES = [
    ("bye", True),
    ("Bye!", True),
    ("ok bye bye", True),
    ("gotta go, see you later", True),
    ("goodnight jarvis", True),
    ("I'm done for now, thanks", True),
    ("exit", True),
    ("catch you later", True),
    ("alright I'm off", True),
    ("peace out jarvis", True),
    ("that's it, close the chat", True),
    ("how do you say bye in french?", False),
    ("write a goodbye message for my coworker who is leaving", False),
    ("my friend said bye and left without paying, was that rude?", False),
    ("what does 'bye bye birdie' mean?", False),
    ("what is the capital of India", False),
    ("tell me a joke about saying goodbye", False),
    ("should I say bye or goodbye in a formal email?", False),
    ("what time should I leave for the airport?", False),
    ("where does 'see you later alligator' come from?", False),
    ("I said bye to my old job today, feeling weird", False),
    ("quiz me on how people say goodbye around the world", False),
]


def main():
    if len(sys.argv) > 1:
        level1_brain.QUIT_MODEL = sys.argv[1]
    model = level1_brain.QUIT_MODEL

    print(f"Loading {model}...")
    wants_to_quit("hello")  # the first call loads the model, so don't time it

    print(f"Testing {model} on {len(CASES)} sentences:\n")
    wrong = 0
    for text, should_quit in CASES:
        start = time.time()
        said_quit = wants_to_quit(text)
        seconds = time.time() - start

        if said_quit == should_quit:
            mark = "ok "
            problem = ""
        elif said_quit:
            mark = "BAD"
            problem = "  <- quit mid-chat!"
        else:
            mark = "BAD"
            problem = "  <- missed a goodbye"
        if mark == "BAD":
            wrong += 1

        print(f"{mark} {seconds:.2f}s  {text}{problem}")

    print(f"\nScore: {len(CASES) - wrong}/{len(CASES)}")


if __name__ == "__main__":
    main()
