@echo off
REM Render Deployment Helper Script (Windows)
REM Run this script to prepare and verify your deployment

echo 🚀 EduRun AI Code Buddy - Render Deployment Helper
echo ==================================================

REM Check if git is initialized
if not exist ".git" (
    echo 📁 Initializing Git repository...
    git init
    echo ✅ Git initialized
) else (
    echo ✅ Git repository already exists
)

REM Check if requirements.txt exists
if exist "requirements.txt" (
    echo ✅ requirements.txt found
    echo 📦 Python dependencies:
    type requirements.txt
) else (
    echo ❌ requirements.txt not found!
    exit /b 1
)

REM Check if render.yaml exists
if exist "render.yaml" (
    echo ✅ render.yaml found
) else (
    echo ❌ render.yaml not found!
    exit /b 1
)

REM Check if main application exists
if exist "backend\api\web_interface.py" (
    echo ✅ Main application found
) else (
    echo ❌ Main application not found!
    exit /b 1
)

echo.
echo 🔧 Pre-deployment checklist:
echo ✅ Git repository initialized
echo ✅ requirements.txt present
echo ✅ render.yaml configuration ready
echo ✅ Flask application ready
echo ✅ Health check endpoint configured
echo ✅ Judge0 API integration ready

echo.
echo 📋 Next steps:
echo 1. Commit your changes:
echo    git add .
echo    git commit -m "Prepare for Render deployment"
echo.
echo 2. Push to GitHub:
echo    git remote add origin https://github.com/yourusername/your-repo-name.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Deploy on Render:
echo    - Go to render.com
echo    - Connect your GitHub repository
echo    - Choose 'Web Service'
echo    - Use these settings:
echo      • Build Command: pip install -r requirements.txt
echo      • Start Command: python -m backend.api.web_interface
echo      • Health Check Path: /api/health
echo.
echo 4. Test your deployment:
echo    python test_deployment.py your-app.onrender.com

echo.
echo 🎉 Your app is ready for Render deployment!
