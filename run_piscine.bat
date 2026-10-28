@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
    py peps_piscine.py %*
) else (
    python peps_piscine.py %*
)
explorer .
pause
