#!/bin/bash
# EduRun AI Code Buddy - Judge0-Only Backend Startup Script
# Platform-Compatible deployment for Railway, Heroku, Render, Vercel

echo "🚀 Starting EduRun AI Code Buddy Backend..."
echo "🏛️ Powered by Judge0 API - Platform Compatible!"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/api/web_interface.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Set environment variables
export FLASK_APP=backend.api.web_interface
export FLASK_ENV=production
export PORT=${PORT:-5000}

echo "📋 Environment:"
echo "   - Flask App: $FLASK_APP"
echo "   - Environment: $FLASK_ENV"
echo "   - Port: $PORT"
echo ""

# Check if Judge0 API key is configured
if [ -z "$RAPIDAPI_KEY" ]; then
    echo "⚠️  Warning: RAPIDAPI_KEY environment variable not set"
    echo "   The app will use a default API key for demo purposes"
    echo ""
fi

# Start the Flask backend
echo "🌐 Starting Flask backend server..."
cd backend
python -m api.web_interface
