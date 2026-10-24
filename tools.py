"""
Jarvis's tools: plain Python functions the model is allowed to ask for.

The model never runs these itself. It reads each function's name, inputs and
docstring, decides which one would help, and asks your code to run it. So
write the docstrings for the model: say what the tool does and when to use it.

Functions starting with _ are helpers, not tools. Jarvis can only use the
ones listed in TOOLS in level3_hands.py.
"""

import difflib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

PROJECTS_FILE = Path(__file__).parent / "projects.json"


# ---------- Everyday ----------

def get_time() -> str:
    """Get the current date and time on the user's Mac."""
    return datetime.now().strftime("%A %d %B %Y, %I:%M:%S %p")


def open_app(app: str) -> str:
    """Open an app on the user's Mac, like Spotify, Safari, Notes or WhatsApp.

    Args:
        app: The app's name, e.g. "Spotify".
    """
    result = subprocess.run(["open", "-a", app], capture_output=True, text=True)
    if result.returncode != 0:
        return f"Couldn't find an app called {app}."
    return f"Opened {app}."


# ---------- Coding projects ----------

def list_projects() -> str:
    """List the names of all the user's coding projects."""
    return ", ".join(_load_projects())


def project_status(project: str) -> str:
    """Check one coding project: its git branch, uncommitted changes, unpushed
    commits and last commit.

    Args:
        project: The project's name, e.g. "jewelix".
    """
    found = _find_project(project)
    if not found:
        return _not_found(project)
    name, path = found

    branch = _git(path, "branch", "--show-current") or "unknown"
    changed = len(_git(path, "status", "--porcelain").splitlines())
    unpushed = _git(path, "rev-list", "--count", "@{u}..HEAD")
    last = _git(path, "log", "-1", "--format=%s (%cr)") or "no commits yet"

    status = f"{name}: on branch {branch}, {changed} uncommitted changes"
    if unpushed and unpushed != "0":
        status += f", {unpushed} commits not pushed"
    return status + f". Last commit: {last}."


def all_projects_status() -> str:
    """Check every coding project at once, most recently worked on first. Use
    this for questions like "what needs attention?" or "what was I working on?"."""
    projects = _load_projects()
    newest_first = sorted(projects, key=lambda name: _git(projects[name], "log", "-1", "--format=%ct") or "0",
                          reverse=True)
    return "\n".join(project_status(name) for name in newest_first)


def open_in_claude(project: str) -> str:
    """Open a coding project in Claude Code, in a new Terminal window.

    Args:
        project: The project's name, e.g. "jewelix".
    """
    found = _find_project(project)
    if not found:
        return _not_found(project)
    name, path = found
    # AppleScript tells the Terminal app to open a window and run a command.
    # The command is passed in separately (argv) so spaces in paths can't break it.
    subprocess.run([
        "osascript",
        "-e", "on run argv",
        "-e", 'tell application "Terminal" to do script (item 1 of argv)',
        "-e", 'tell application "Terminal" to activate',
        "-e", "end run",
        f"cd '{path}' && claude",
    ], capture_output=True)
    return f"Opened {name} in Claude Code."


def open_in_vscode(project: str) -> str:
    """Open a coding project in VS Code.

    Args:
        project: The project's name, e.g. "jewelix".
    """
    found = _find_project(project)
    if not found:
        return _not_found(project)
    name, path = found
    subprocess.run(["open", "-a", "Visual Studio Code", path], capture_output=True)
    return f"Opened {name} in VS Code."


# ---------- Helpers (not tools) ----------

def _load_projects():
    """Read projects.json: {"project name": "/path/to/folder"}."""
    return json.loads(PROJECTS_FILE.read_text())


def _simplify(name):
    """'TAHI-2.O' -> 'tahi2o', so spoken names match folder names."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _find_project(spoken_name):
    """Match a name, maybe misheard by Whisper, to a real project.
    Returns (name, path), or None if nothing is close enough."""
    projects = _load_projects()
    by_simple_name = {_simplify(name): name for name in projects}
    match = difflib.get_close_matches(_simplify(spoken_name), by_simple_name, n=1, cutoff=0.6)
    if not match:
        return None
    name = by_simple_name[match[0]]
    return name, projects[name]


def _not_found(spoken_name):
    return f"There's no project called {spoken_name}. The projects are: {list_projects()}."


def _git(path, *args):
    """Run a git command in a project folder and return what it printed."""
    result = subprocess.run(["git", "-C", path, *args], capture_output=True, text=True)
    return result.stdout.strip()
