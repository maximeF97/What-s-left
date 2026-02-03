#!/bin/bash
# macOS launcher for What's Left game
# This script can be used to create a .app bundle on macOS

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Get Python executable
if [ -x ".venv/bin/python" ]; then
    PYTHON_EXE=".venv/bin/python"
else
    PYTHON_EXE="python3"
fi

# Launch the game using open command on macOS
nohup "$PYTHON_EXE" launch.py > /dev/null 2>&1 &

exit 0
