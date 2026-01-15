@echo off
setlocal

:: Get directory of this script
set "SCRIPT_DIR=%~dp0"
set "PYTHON_CMD=python"
set "TASK_NAME=CodeToPlay_Warden"

:: 1. Install Dependencies
echo [INFO] Installing Python dependencies...
"%PYTHON_CMD%" -m pip install -r "%SCRIPT_DIR%requirements.txt"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

:: 2. Register Scheduled Task (The Warden)
:: Runs visible output first time for testing, but in production usually pythonw.
:: For now, we use pythonw to hide console.
echo [INFO] Registering Task: %TASK_NAME%
schtasks /create /tn "%TASK_NAME%" /tr "\"%PYTHON_CMD%w\" \"%SCRIPT_DIR%warden.py\"" /sc onlogon /rl highest /f

echo [INFO] Setup Complete.
echo [INFO] To start monitoring immediately, run: schtasks /run /tn "%TASK_NAME%"
echo [IMPORTANT] Ensure 'GEMINI_API_KEY' is set in your user environment variables for the Auditor to work.
pause
