"""
Level 1: Brain. A chat loop with a model running on your own Mac.

Run it:  uv run level1_brain.py
Quit:    type "bye"
"""

import ollama

MODEL = "llama3.1:8b"
QUIT_MODEL = "qwen3-coder:30b"

QUIT_CHECK_PROMPT = """You decide whether a message means the user wants to end the chat right now.
Reply with only YES or NO.

Examples:
"bye" -> YES
"ok thanks, that's all for today" -> YES
"heading out now, talk tomorrow" -> YES
"how do you say bye in Spanish?" -> NO
"write a goodbye card for my coworker" -> NO"""

# STEP 4: Give Jarvis a personality. Write instructions here: who it is,
# how long its answers should be, what tone to use.
SYSTEM_PROMPT =  """You are Jarvis, a annooyed assistant running on the user's Mac. Keep answers short.

When the user asks for a quiz:
- Ask ONE question at a time, with options A to D. Then stop and wait for their answer.
- When they answer, say whether they were right or wrong and give the correct answer.
- Then ask the next question. After 5 questions, tell them their score."""


def ask(messages):
    """Send the conversation to the model and return its reply as text."""
    # STEP 1: call ollama.chat with MODEL and messages, then return the reply text.
    # STEP 5: switch to streaming, so words appear as they're generated.
    response = ollama.chat(model=MODEL, messages=messages)
    return response.message.content

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

    # STEP 3: this list will become Jarvis's memory.
    history = [{"role": "system", "content": SYSTEM_PROMPT}]

   
    
    #
    # STEP 2: replace that with a loop that reads what you type with input().
    while True:
        text = input("You: ")
        if text == "bye":
            break
        history.append({"role": "user", "content": text})
        reply = ask(history)
        print("Jarvis:", reply)
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
