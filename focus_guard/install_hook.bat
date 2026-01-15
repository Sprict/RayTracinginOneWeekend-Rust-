@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "HOOK_SRC=%SCRIPT_DIR%post-commit"
set "HOOK_DEST=%SCRIPT_DIR%..\.git\hooks\post-commit"

echo [INFO] Installing Git Hook...
copy /Y "%HOOK_SRC%" "%HOOK_DEST%"

if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Hook installed to .git\hooks\post-commit
) else (
    echo [ERROR] Failed to install hook. Make sure you are in the project root.
)
pause
