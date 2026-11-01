@echo off
cd /d "%~dp0"
echo Open http://127.0.0.1:8000 in your browser. Press Ctrl+C here to stop.
python server.py
pause
