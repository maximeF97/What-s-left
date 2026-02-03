#!/usr/bin/env bash

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the project directory
cd "$SCRIPT_DIR"

# Launch the GUI using venv Python if available
if [ -x ".venv/bin/python" ]; then
    exec ".venv/bin/python" run_gui.py
else
    exec python3 run_gui.py
fi
