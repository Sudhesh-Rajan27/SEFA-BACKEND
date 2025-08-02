@echo off
REM EduRun AI Code Buddy - Judge0-Only Backend Startup Script (Windows)
REM Platform-Compatible deployment for Railway, Heroku, Render, Vercel

echo 🚀 Starting EduRun AI Code Buddy Backend...
echo 🏛️ Powered by Judge0 API - Platform Compatible!
echo.

REM Check if we're in the right directory
if not exist "backend\api\web_interface.py" (
    echo ❌ Error: Please run this script from the project root directory
    exit /b 1
)

REM Set environment variables
set FLASK_APP=backend.api.web_interface
set FLASK_ENV=production
if not defined PORT set PORT=5000

echo 📋 Environment:
echo    - Flask App: %FLASK_APP%
echo    - Environment: %FLASK_ENV%
echo    - Port: %PORT%
echo.

REM Check if Judge0 API key is configured
if not defined RAPIDAPI_KEY (
    echo ⚠️  Warning: RAPIDAPI_KEY environment variable not set
    echo    The app will use a default API key for demo purposes
    echo.
)

REM Start the Flask backend
echo 🌐 Starting Flask backend server...
cd backend
python -m api.web_interface
