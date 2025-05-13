@echo off
REM Safe Runner for Logic Tool
REM This batch file makes it easy to run Logic Tool commands with the safe wrapper

REM Install psutil if not already installed
pip install psutil -q

REM Run the command with the safe wrapper
python safe_run.py %*

echo.
echo Command execution complete.
