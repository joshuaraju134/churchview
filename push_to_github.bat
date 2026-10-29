@echo off
title Push ChurchView to GitHub
cd /d "%~dp0"
set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%PATH%"

echo ==========================================================
echo   Pushing ChurchView with 1,054 Songs to GitHub...
echo   Repository: https://github.com/joshuaraju134/churchview
echo ==========================================================
echo.

git push -u origin main --force

echo.
if %ERRORLEVEL% equ 0 (
    echo ==========================================================
    echo   [SUCCESS] All 1,054 songs & clean UI pushed to GitHub!
    echo ==========================================================
) else (
    echo ==========================================================
    echo   [NOTICE] If a browser login window opened, please
    echo   click "Authorize" in your browser, then run this again.
    echo ==========================================================
)
echo.
pause
