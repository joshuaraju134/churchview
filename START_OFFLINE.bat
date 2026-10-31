@echo off
cd /d "%~dp0"
title ChurchView Offline
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0offline_server.ps1"
pause
