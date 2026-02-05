@echo off
REM Windows launcher for What's Left game
REM Icon file: assets\game_icon.ico

echo ===============================================
echo    What's Left - Starting Game...
echo ===============================================
echo.

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located (Windows path)
set SCRIPT_DIR=%~dp0

REM Handle UNC paths by converting them to drive letters if possible
pushd "%SCRIPT_DIR%" 2>nul
if errorlevel 1 (
    echo ERROR: Cannot access game directory
    echo Path: %SCRIPT_DIR%
    echo.
    echo This might be a UNC path issue.
    echo Please run this batch file from a mapped drive or local folder.
    pause
    exit /b 1
)

REM Now we're in the correct directory
echo Game directory: %CD%
echo.

REM Check for Python in multiple locations
set PYTHON_EXE=

REM 1. Check virtual environment
if exist ".venv\Scripts\python.exe" (
    set PYTHON_EXE=.venv\Scripts\python.exe
    echo Found: Virtual environment Python
    goto :run_game
)

REM 2. Check for py launcher (Windows Python Launcher)
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXE=py
    echo Found: Python Launcher (py)
    goto :run_game
)

REM 3. Check for python3 in PATH
where python3 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXE=python3
    echo Found: python3
    goto :run_game
)

REM 4. Check for python in PATH
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    REM Make sure it's not the Windows Store stub
    python --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_EXE=python
        echo Found: python
        goto :run_game
    )
)

REM No Python found
echo.
echo ===============================================
echo ERROR: Python not found!
echo ===============================================
echo.
echo Please install Python 3.8 or higher:
echo   1. Download from: https://www.python.org/downloads/
echo   2. Or install from Microsoft Store
echo   3. Make sure to check "Add Python to PATH" during installation
echo.
pause
exit /b 1

:run_game
echo.
echo Launching game with: %PYTHON_EXE%
echo.
"%PYTHON_EXE%" run_gui.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ===============================================
    echo ERROR: Game failed to launch. See error above.
    echo ===============================================
    echo.
    pause
)

popd
exit /b 0