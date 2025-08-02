# EduRun AI Code Buddy - Frontend & Backend Integration

## 🚀 Complete Setup Guide

This project consists of two main components:
1. **Backend API** (Flask + Judge0) - Multi-language code execution
2. **Frontend** (React + TypeScript) - Interactive code editor

## 📋 Prerequisites

- **Python 3.8+** with virtual environment
- **Node.js 16+** and npm
- **Judge0 API Key** (included in backend)

## 🔧 Installation & Setup

### 1. Backend Setup (Judge0 API)

```bash
# Navigate to the root directory
cd s:\SEFA

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (already done)
pip install -r requirements.txt

# Start the backend server
python backend/api/web_interface.py
```

**Backend will run on:** `http://localhost:5000`

### 2. Frontend Setup (React App)

```bash
# Navigate to frontend directory  
cd s:\SEFA\edurun-ai-code-buddy-76

# Install dependencies (if needed)
npm install

# Start development server
npm run dev
```

**Frontend will run on:** `http://localhost:8080`

## 🌐 API Integration

The frontend automatically connects to the backend API running on `localhost:5000`. 

### Environment Configuration

- **Development:** Uses `.env.development` (localhost:5000)
- **Production:** Uses `.env.production` (your deployed backend URL)

## 🎯 Features

### ✅ Supported Languages
- **Python 3.8.1** - Full execution via Judge0
- **JavaScript (Node.js 12.14.0)** - Server-side execution
- **C++ (GCC 9.2.0)** - Compilation and execution
- **Java, C#, Go, Rust, PHP, Ruby** - Also supported

### 🔧 Core Features
- **Real-time Code Execution** - Via Judge0 API
- **Language Auto-detection** - Smart detection from code patterns
- **Error Handling** - Comprehensive error reporting
- **Execution Metrics** - Runtime and performance data
- **Backend Health Monitoring** - Connection status indicators
- **Code Saving** - Save and load code snippets
- **AI Feedback** - Code analysis and suggestions

## 🖥️ Usage Instructions

### 1. Start Both Servers

1. **Start Backend:**
   ```bash
   # Terminal 1
   cd s:\SEFA
   venv\Scripts\activate
   python backend/api/web_interface.py
   ```

2. **Start Frontend:**
   ```bash
   # Terminal 2  
   cd s:\SEFA\edurun-ai-code-buddy-76
   npm run dev
   ```

### 2. Access the Application

- Open `http://localhost:8080` in your browser
- Click "Get Started" or navigate to "/editor"
- Check the "Backend Connected" status indicator

### 3. Write and Execute Code

1. **Select Language:** Choose from JavaScript, Python, or C++
2. **Write Code:** Use the built-in Monaco editor
3. **Run Code:** Click "Run Code" (requires backend connection)
4. **View Results:** Check output panel for execution results

## 🔗 API Endpoints

### Backend API (localhost:5000)

- `POST /api/compile` - Execute code
- `GET /api/health` - Backend health check
- `GET /api/languages` - Supported languages
- `POST /compile` - Legacy endpoint

### Sample API Request

```javascript
// Execute Python code
const response = await fetch('http://localhost:5000/api/compile', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: 'print("Hello, World!")',
    language: 'python'
  })
});

const result = await response.json();
console.log(result.output); // ["Hello, World!"]
```

## 🛠️ Development 

### Frontend Development
- Built with React 18 + TypeScript + Vite
- Uses TanStack Query for API state management
- Styled with Tailwind CSS + shadcn/ui components
- Monaco Editor for code editing

### Backend Development  
- Flask REST API with CORS support
- Judge0 integration for secure code execution
- Platform-compatible (Railway, Heroku, Vercel)
- Comprehensive logging and error handling

## 🚀 Deployment

### Development
Both servers run locally for development:
- Frontend: `http://localhost:8080`
- Backend: `http://localhost:5000`

### Production
1. Deploy backend to Railway/Heroku/Render
2. Deploy frontend to Vercel/Netlify
3. Update `VITE_API_URL` in `.env.production`

## 🔍 Troubleshooting

### Backend Issues
- **"Judge0 compiler not available"** - Check API key in `judge0_compiler.py`
- **Connection failed** - Ensure backend runs on port 5000
- **CORS errors** - Backend includes CORS headers for localhost:8080

### Frontend Issues  
- **"Backend Offline"** - Start backend server first
- **Build errors** - Run `npm install` to update dependencies
- **Port conflicts** - Change port in `vite.config.ts` if needed

## 📊 Status Indicators

- 🟢 **Backend Connected** - Judge0 API accessible
- 🔴 **Backend Offline** - Cannot reach backend server  
- 🟡 **Checking...** - Connection status being verified

## 🔐 Security

- **Sandboxed Execution** - All code runs in Judge0's secure environment
- **No Local Execution** - Frontend doesn't execute code locally
- **API Rate Limiting** - Judge0 handles request throttling
- **Input Validation** - Backend validates all code submissions

## 📈 Performance

- **Execution Time:** 2-4 seconds average (Judge0 processing)
- **Memory Limit:** 128MB per execution
- **Timeout:** 30 seconds default
- **Concurrent Users:** Supported via Judge0 infrastructure

---

## 🎉 Ready to Code!

Your integrated frontend and backend are now set up and running. The React frontend communicates seamlessly with your Flask backend, which executes code using the Judge0 API for secure, multi-language code execution.

**Test the integration:**
1. Go to `http://localhost:8080/editor`
2. Write some Python/JavaScript/C++ code
3. Click "Run Code" and see the results!

Happy coding! 🚀
