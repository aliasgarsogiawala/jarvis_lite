"""
Level 3: Hands. Talk to Jarvis and it does things on your Mac.

Run it:  uv run level3_hands.py          (talk to it)
         uv run level3_hands.py --text   (type instead, handy for testing)
Quit:    say "bye"
"""

import json
import sys
from datetime import datetime

import ollama

import tools
from ears import is_silent, record
from level1_brain import MODEL, wants_to_quit
from level2_voice import VOICE_PROMPT, hear, speak
from spinner import Spinner

# The menu: the only tools Jarvis can ever use.
TOOLS = [
    tools.get_time,
    tools.open_app,
    tools.list_projects,
    tools.project_status,
    tools.all_projects_status,
    tools.open_in_claude,
    tools.open_in_vscode,
]

HANDS_PROMPT = VOICE_PROMPT + """

You can control the user's Mac with tools. When they ask you to do something,
use a tool, then confirm what you did in one short sentence."""

TEXT_MODE = "--text" in sys.argv
LOG_FILE = "activity_log.jsonl"


def listen():
    """Get the user's next message: typed in text mode, spoken otherwise."""
    if TEXT_MODE:
        return input("You: ")
    while True:
        audio = record()
        if not is_silent(audio):
            text = hear(audio)
            print(f"You: {text}")
            return text
        print("(didn't hear anything)")


def reply(text):
    """Show Jarvis's answer, and say it out loud unless we're in text mode."""
    if TEXT_MODE:
        print("Jarvis:", text)
    else:
        print("Jarvis:")
        speak(text)


def run_tool(call):
    """Run the tool Jarvis asked for and return what it gave back."""
    name = call.function.name
    args = call.function.arguments
    print(f"  🔧 {name}({', '.join(f'{k}={v!r}' for k, v in args.items())})")
    allowed = {tool.__name__: tool for tool in TOOLS}
    if name not in allowed:
        return f"There is no tool called {name}."
    return str(allowed[name](**args))


def think(history):
    """Your Part 4, upgraded. Jarvis can now use several tools in a row, e.g.
    check every project, then open the busiest one. Keep running whatever it
    asks for until it answers in words. This loop is what makes it an agent.
    Returns (answer, names of the tools it used)."""
    used = []
    while True:
        spinner = Spinner()
        spinner.start()
        response = ollama.chat(model=MODEL, messages=history, tools=TOOLS)
        spinner.stop()
        history.append(response.message)

        if not response.message.tool_calls:
            # qwen sometimes leaves a stray "<tool_call>" at the end of its answer.
            return response.message.content.replace("<tool_call>", "").strip(), used

        for call in response.message.tool_calls:
            result = run_tool(call)
            used.append(call.function.name)
            history.append({"role": "tool", "content": result, "tool_name": call.function.name})


def log(said, used):
    """Note down what you asked and which tools ran. Level 5 learns your routine from this."""
    entry = {"time": datetime.now().isoformat(timespec="seconds"), "said": said, "tools": used}
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    mode = "typing" if TEXT_MODE else "listening"
    print(f"Jarvis has hands and is {mode}, running {MODEL}. Say 'bye' to quit.\n")
    history = [{"role": "system", "content": HANDS_PROMPT}]

    while True:
        text = listen()
        quitting = wants_to_quit(text)
        history.append({"role": "user", "content": text})
        answer, used = think(history)
        reply(answer)
        log(text, used)
        if quitting:
            break


if __name__ == "__main__":
    main()
