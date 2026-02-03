#!/usr/bin/env python3
"""
Cross-platform launcher for What's Left game.
Works on Linux, Windows, and macOS with the same entry point.
Includes icon support for all platforms.
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


def get_project_dir():
    """Get the absolute path to the project directory."""
    return Path(__file__).parent.absolute()


def get_python_executable():
    """Get the path to the Python executable."""
    # Use the venv Python if available, otherwise system Python
    project_dir = get_project_dir()
    
    # On Windows, prefer pythonw.exe for GUI apps (no console window)
    if platform.system() == "Windows":
        venv_paths = [
            project_dir / ".venv" / "Scripts" / "pythonw.exe",  # Windows venv GUI
            project_dir / ".venv" / "Scripts" / "python.exe",   # Windows venv fallback
        ]
    else:
        venv_paths = [
            project_dir / ".venv" / "bin" / "python",  # Unix venv
        ]
    
    for venv_path in venv_paths:
        if venv_path.exists():
            return str(venv_path)
    
    # Fallback to system Python (pythonw on Windows if available)
    if platform.system() == "Windows":
        import shutil
        pythonw = shutil.which("pythonw")
        if pythonw:
            return pythonw
    
    return sys.executable


def launch_gui():
    """Launch the GUI on any platform."""
    project_dir = get_project_dir()
    python_exe = get_python_executable()
    
    # Change to project directory
    os.chdir(project_dir)
    
    # Prepare the command
    cmd = [python_exe, "run_gui.py"]
    
    try:
        if platform.system() == "Windows":
            # Windows: detach from console
            subprocess.Popen(
                cmd,
                cwd=project_dir,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            # Linux/macOS: use nohup to detach
            subprocess.Popen(
                cmd,
                cwd=project_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
    except Exception as e:
        print(f"Error launching game: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    launch_gui()
