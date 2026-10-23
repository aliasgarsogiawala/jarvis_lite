"""
Jarvis's tools: plain Python functions the model is allowed to ask for.

The model never runs these itself. It reads each function's name, inputs and
docstring, decides which one would help, and asks your code to run it. So
write the docstrings for the model: say what the tool does and when to use it.
"""

from datetime import datetime


# STEP 1: your first tool, get_time().
