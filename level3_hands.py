"""
Level 3: Hands. Jarvis can do things, not just talk.

Run it:  uv run level3_hands.py
Quit:    type "bye"
"""

import ollama

import tools
from level1_brain import MODEL, SYSTEM_PROMPT, wants_to_quit

# STEP 1: the tools Jarvis is allowed to use.
TOOLS = []


def run_tool(call):
    """Run the tool the model asked for and return its result as text."""
    # STEP 2: look up the function by name and call it with the model's arguments.
    pass


def think(history):
    """Let the model use tools until it has an answer, then return the answer."""
    # STEP 2: the agent loop.
    pass


def main():
    print(f"Jarvis has hands, running {MODEL}. Type 'bye' to quit.\n")
    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        text = input("You: ")
        if wants_to_quit(text):
            print("Jarvis: See you later!")
            break
        history.append({"role": "user", "content": text})
        # STEP 1: call ollama.chat with tools=TOOLS and print what comes back.
        # STEP 2: replace that with think(history).


if __name__ == "__main__":
    main()
