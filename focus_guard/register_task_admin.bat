@echo off
:: このバッチファイルを「管理者として実行」してください
cd /d "%~dp0"

echo ========================================================
echo   FocusGuard タスク登録ウィザード
echo ========================================================
echo.

:: 管理者権限チェック
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 管理者権限が必要です。
    echo 右クリックして「管理者として実行」してください。
    pause
    exit /b
)

echo FocusGuardをタスクスケジューラに登録しています...
echo パス: "%~dp0guard.ps1"

:: タスクの作成 (ログオン時に起動)
schtasks /create /tn "FocusGuard" /tr "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File '%~dp0guard.ps1'" /sc onlogon /f

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] タスクが正常に登録されました！
    echo 次回のログイン時から自動的に起動します。
    echo.
    echo 今すぐ起動しますか？ (何かキーを押すと起動します)
    pause >nul
    schtasks /run /tn "FocusGuard"
) else (
    echo.
    echo [FAILURE] タスクの登録に失敗しました。
)

pause
