#!/usr/bin/env bash

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the project directory
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Launch the GUI
exec python3 run_gui.py
