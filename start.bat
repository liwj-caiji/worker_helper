@echo off
chcp 65001 >nul

echo === Experience Factory ===
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.

echo Starting backend...
start "EF-Backend" cmd /k "uv run uvicorn backend.main:app --reload"

echo Starting frontend...
start "EF-Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo Both servers started.
echo Close this window and the two server windows to stop.
pause
