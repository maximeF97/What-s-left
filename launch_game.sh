#!/usr/bin/env bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the project directory
cd "$SCRIPT_DIR"

# Launch the GUI using venv Python if available, detached from terminal
if [ -x ".venv/bin/python" ]; then
    nohup ".venv/bin/python" run_gui.py > /dev/null 2>&1 &
else
    nohup python3 run_gui.py > /dev/null 2>&1 &
fi

# Return immediately so the launcher doesn't hang
exit 0
