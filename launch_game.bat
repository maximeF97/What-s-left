@echo off
REM Windows launcher for What's Left game
REM This script launches the game GUI on Windows
REM Icon file: assets\game_icon.ico

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

REM Change to the project directory
cd /d "%SCRIPT_DIR%"

REM Check if venv Python exists, otherwise use system Python
if exist ".venv\Scripts\python.exe" (
    set PYTHON_EXE=.venv\Scripts\python.exe
) else (
    set PYTHON_EXE=python
)

REM Launch the game in the background
start "" %PYTHON_EXE% launch.py

REM Exit immediately
exit /b 0
