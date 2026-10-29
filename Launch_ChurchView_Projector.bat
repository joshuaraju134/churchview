@echo off
title ChurchView Pro - Church of God Alappuzha Town
cd /d "%~dp0"

echo ==========================================================
echo   Starting ChurchView Pro Dual Bible Projector...
echo   Church of God (Full Gospel) in India, Alappuzha Town
echo ==========================================================
echo.

where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Launching with Python...
    python server.py
    goto end
)

where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Launching with Python Launcher...
    py server.py
    goto end
)

echo [INFO] Python not detected. Launching via Windows PowerShell...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0server_ps.ps1"

:end
pause
