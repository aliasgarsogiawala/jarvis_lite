"""
Level 1: Brain. A chat loop with a model running on your own Mac.

Run it:  uv run level1_brain.py
Quit:    type "bye"
"""

import ollama
from spinner import Spinner

MODEL = "qwen3-coder:30b"
QUIT_MODEL = "qwen3-coder:30b"

QUIT_CHECK_PROMPT = """You decide whether a message means the user wants to end the chat right now.
Reply with only YES or NO.

Examples:
"bye" -> YES
"ok thanks, that's all for today" -> YES
"heading out now, talk tomorrow" -> YES
"how do you say bye in Spanish?" -> NO
"write a goodbye card for my coworker" -> NO"""


SYSTEM_PROMPT =  """You are Jarvis, a annooyed assistant running on the user's Mac. Keep answers short.

When the user asks for a quiz:
- Ask ONE question at a time, with options A to D. Then stop and wait for their answer.
- When they answer, say whether they were right or wrong and give the correct answer.
- Then ask the next question. After 5 questions, tell them their score."""


def ask(messages):
    """Send the conversation to the model, print the reply as it arrives, and return it."""
    spinner = Spinner()                  # new
    spinner.start()                      # new
    reply = ""
    for chunk in ollama.chat(model=MODEL, messages=messages, stream=True):
        piece = chunk.message.content
        if piece and not reply:          # new
            spinner.stop()               # new
            print("Jarvis: ", end="")    # new
        print(piece, end="", flush=True)
        reply += piece
        if chunk.done:
            speed = chunk.eval_count / (chunk.eval_duration / 1e9)
            print(f"\n[{chunk.eval_count} tokens, {speed:.0f} tokens/sec]", end="")
    spinner.stop()                       # new
    print()
    return reply

def wants_to_quit(text):
    """Ask a model whether this message means 'I'm leaving'."""
    response = ollama.chat(
        model=QUIT_MODEL,
        messages=[
            {"role": "system", "content": QUIT_CHECK_PROMPT},
            {"role": "user", "content": text},
        ],
        options={"temperature": 0},
    )
    return response.message.content.strip().upper().startswith("YES")

def main():
    print(f"Jarvis is online, running {MODEL}. Type 'bye' to quit.\n")

    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        text = input("You: ")
        if wants_to_quit(text):
            print("Jarvis: See you later!")
            break
        history.append({"role": "user", "content": text})
        reply = ask(history)
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
