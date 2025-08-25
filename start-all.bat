@echo off
title Healthcare Assistant - All Services
color 0A

echo.
echo ========================================
echo   Healthcare Assistant - Service Launcher
echo ========================================
echo.

echo [INFO] Starting all services...
echo.

REM Start AI Service in new window
echo [1/3] Starting AI Service (Port 5001)...
start "AI Service" cmd /k "cd /d ai_service && python app.py"
timeout /t 5 /nobreak >nul

REM Start Backend Server in new window  
echo [2/3] Starting Backend Server (Port 5000)...
start "Backend Server" cmd /k "cd /d server && node index.js"
timeout /t 5 /nobreak >nul

REM Start React Frontend in new window
echo [3/3] Starting React Frontend (Port 3000)...
start "React Frontend" cmd /k "cd /d client && npm start"

echo.
echo ========================================
echo   All Services Started Successfully!
echo ========================================
echo.
echo Frontend:   http://localhost:3000
echo Backend:    http://localhost:5000  
echo AI Service: http://localhost:5001
echo.
echo Press any key to open the application...
pause >nul

REM Open the application in default browser
start http://localhost:3000

echo.
echo Application opened in browser.
echo Close this window when done.
echo.
pause
