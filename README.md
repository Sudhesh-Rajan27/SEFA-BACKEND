# EduRun AI Code Buddy - Production Ready

## 🏛️ Judge0-Powered Code Execution Platform

A **Docker-free**, **platform-compatible** code execution service powered by Judge0 API. Deploy anywhere - Railway, Heroku, Vercel, AWS, or any Python-supporting platform.

### ✨ Features

- 🌍 **Universal Deployment** - No Docker requirements
- 🏛️ **Judge0 API Integration** - Professional sandboxed execution  
- 🚀 **Multi-Language Support** - Python, JavaScript, C++, Java, C#, Go, Rust, PHP, Ruby
- 🔧 **REST API** - Clean endpoints for frontend integration
- 📊 **Auto Language Detection** - Smart programming language detection
- ⚡ **Production Ready** - Health monitoring, error handling, CORS support

### 🚀 Quick Start

#### Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the backend
./start_judge0_backend.sh    # Linux/Mac
start_judge0_backend.bat     # Windows

# 3. Test the API
curl -X POST http://localhost:5000/api/compile \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello World!\")", "language": "python"}'
```

#### Deploy to Railway
```bash
railway login
railway init
railway up
```

#### Deploy to Heroku
```bash
heroku create your-app-name
git push heroku main
```

### 📡 API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/api/compile` | POST | Execute code |
| `/api/health` | GET | Health check |
| `/api/languages` | GET | Supported languages |

### 📁 Project Structure

```
📦 EduRun AI Code Buddy
├── 📁 backend/
│   ├── 📁 api/
│   │   └── 📄 web_interface.py      # Main Flask application
│   └── 📁 compilers/
│       └── 📄 judge0_compiler.py    # Judge0 API integration
├── 📄 requirements.txt              # Python dependencies
├── 📄 railway.toml                  # Railway deployment config
├── 📄 start_judge0_backend.sh       # Linux/Mac startup
├── 📄 start_judge0_backend.bat      # Windows startup
└── 📄 README.md                     # This file
```

### 🔧 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RAPIDAPI_KEY` | No | Demo key | Your RapidAPI key for Judge0 |
| `PORT` | No | 5000 | Server port |
| `FLASK_ENV` | No | production | Flask environment |

### 🌟 Supported Languages

- **Python** 3.8.1
- **JavaScript** (Node.js 12.14.0)  
- **C++** (GCC 9.2.0)
- **C** (GCC 9.2.0)
- **Java** (OpenJDK 13.0.1)
- **C#** (Mono 6.6.0.161)
- **Go** (1.13.5)
- **Rust** (1.40.0)
- **PHP** (7.4.1)
- **Ruby** (2.7.0)

### 📞 Support

Visit `/api/health` for system status and diagnostics.

---

**🎉 Ready for production deployment on any platform!**
