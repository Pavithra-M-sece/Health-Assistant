@echo off
setlocal enabledelayedexpansion

echo 🚀 Healthcare Assistant App - Windows Deployment
echo ================================================

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Please run this script as Administrator
    pause
    exit /b 1
)

REM Create application directory
set APP_DIR=C:\healthcare-assistant
echo 📁 Creating application directory: %APP_DIR%
if not exist "%APP_DIR%" mkdir "%APP_DIR%"

REM Copy application files
echo 📋 Copying application files...
xcopy /E /I /Y . "%APP_DIR%"

cd /d "%APP_DIR%"

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.7+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Create Python virtual environment
echo 🐍 Setting up Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📦 Installing Python dependencies...
cd ai_service
pip install -r requirements.txt
cd ..

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
cd server
call npm install --production
cd ..

cd client
call npm install --production
call npm run build
cd ..

REM Create Windows services
echo ⚙️ Creating Windows services...

REM Create backend service
sc create "HealthcareBackend" binPath= "C:\Program Files\nodejs\node.exe %APP_DIR%\server\index.js" start= auto
sc description "HealthcareBackend" "Healthcare Assistant Backend Service"

REM Create AI service
sc create "HealthcareAI" binPath= "%APP_DIR%\venv\Scripts\python.exe %APP_DIR%\ai_service\new_backend.py" start= auto
sc description "HealthcareAI" "Healthcare Assistant AI Service"

REM Create management script
echo 📝 Creating management script...
(
echo @echo off
echo setlocal
echo.
echo if "%%1"=="start" ^(
echo     echo Starting services...
echo     sc start HealthcareBackend
echo     sc start HealthcareAI
echo     echo ✅ Services started
echo ^) else if "%%1"=="stop" ^(
echo     echo Stopping services...
echo     sc stop HealthcareBackend
echo     sc stop HealthcareAI
echo     echo 🛑 Services stopped
echo ^) else if "%%1"=="restart" ^(
echo     echo Restarting services...
echo     sc stop HealthcareBackend
echo     sc stop HealthcareAI
echo     timeout /t 5 /nobreak ^>nul
echo     sc start HealthcareBackend
echo     sc start HealthcareAI
echo     echo 🔄 Services restarted
echo ^) else if "%%1"=="status" ^(
echo     echo Backend service status:
echo     sc query HealthcareBackend
echo     echo.
echo     echo AI service status:
echo     sc query HealthcareAI
echo ^) else ^(
echo     echo Usage: %%0 {start^|stop^|restart^|status^}
echo     exit /b 1
echo ^)
) > "%APP_DIR%\manage.bat"

echo.
echo 🎉 Deployment completed successfully!
echo.
echo 📍 Application URLs:
echo    • Frontend: http://localhost:3000
echo    • Backend API: http://localhost:5000
echo    • AI Service: http://localhost:5000
echo.
echo 🔧 Management commands:
echo    • Start services: %APP_DIR%\manage.bat start
echo    • Stop services:  %APP_DIR%\manage.bat stop
echo    • Restart services: %APP_DIR%\manage.bat restart
echo    • Check status: %APP_DIR%\manage.bat status
echo.
echo 📋 Next steps:
echo    1. Start the services using: %APP_DIR%\manage.bat start
echo    2. Configure IIS or another web server for production
echo    3. Set up SSL certificates
echo    4. Configure firewall rules
echo.
pause 