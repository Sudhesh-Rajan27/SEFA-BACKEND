# EduRun AI Code Buddy - Render Deployment Guide

## 🚀 Deploy to Render

This guide will help you deploy your Judge0-powered code execution platform to Render.

### ✅ Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Judge0 API Access** - Already configured in the project

### 📁 Required Files (Already Created)

- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render deployment configuration  
- ✅ `backend/api/web_interface.py` - Main Flask application
- ✅ Health check endpoint at `/api/health`

### 🔧 Deployment Steps

#### Step 1: Prepare Your Repository

1. **Push to GitHub:**
   ```bash
   # Initialize git if not already done
   git init
   git add .
   git commit -m "Initial commit for Render deployment"
   
   # Add your GitHub repository
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

#### Step 2: Deploy on Render

1. **Go to Render Dashboard:**
   - Visit [render.com](https://render.com)
   - Sign in with your GitHub account

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure Service:**
   ```
   Name: sefa-back (or your preferred name)
   Region: Choose closest to your users
   Branch: main
   Root Directory: (leave blank)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python -m backend.api.web_interface
   ```

4. **Environment Variables:**
   Add these in the Render dashboard:
   ```
   FLASK_ENV=production
   PYTHONPATH=/opt/render/project/src
   ```
   
   Optional (for enhanced Judge0 features):
   ```
   RAPIDAPI_KEY=your-rapidapi-key-here
   ```

5. **Health Check:**
   ```
   Health Check Path: /api/health
   ```

#### Step 3: Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start your Flask application
   - Assign a public URL

### 🌐 Access Your Deployed API

Once deployed, your API will be available at:
```
https://your-service-name.onrender.com
```

### 📊 Test Your Deployment

```bash
# Test health endpoint
curl https://your-service-name.onrender.com/api/health

# Test code execution
curl -X POST https://your-service-name.onrender.com/api/compile \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello from Render!\")", "language": "python"}'

# Get supported languages
curl https://your-service-name.onrender.com/api/languages
```

### ⚙️ Service Configuration

Your `render.yaml` file configures:

- **Service Type:** Web service
- **Environment:** Python
- **Plan:** Starter (free tier)
- **Auto-deploy:** Enabled on git push
- **Health Checks:** Automatic monitoring
- **HTTPS:** Automatically provided

### 🔄 Continuous Deployment

Render automatically redeploys when you push to your main branch:

```bash
# Make changes to your code
git add .
git commit -m "Update application"
git push origin main
# Render automatically deploys the changes
```

### 📈 Monitoring & Logs

1. **View Logs:**
   - Go to your service dashboard
   - Click "Logs" tab
   - Monitor real-time application logs

2. **Monitor Health:**
   - Health checks run automatically
   - Service restarts if health check fails
   - View metrics in the dashboard

### 🛠️ Troubleshooting

#### Common Issues:

1. **Build Fails:**
   - Check `requirements.txt` format
   - Ensure all dependencies are listed
   - View build logs for specific errors

2. **Health Check Fails:**
   - Verify `/api/health` endpoint works locally
   - Check if application starts correctly
   - Review application logs

3. **Import Errors:**
   - Ensure `PYTHONPATH` is set correctly
   - Check file structure and import statements

4. **Judge0 API Issues:**
   - Add your own `RAPIDAPI_KEY` environment variable
   - Check Judge0 API status
   - Review API response logs

### 🔒 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FLASK_ENV` | Yes | Set to `production` |
| `PYTHONPATH` | Yes | Set to `/opt/render/project/src` |
| `RAPIDAPI_KEY` | No | Your Judge0 API key (uses demo key if not set) |
| `PORT` | No | Auto-set by Render |

### 💰 Pricing

- **Starter Plan:** Free with limitations
  - 750 hours/month
  - Service spins down after 15 minutes of inactivity
  - Slower cold starts

- **Paid Plans:** Starting at $7/month
  - Always-on service
  - Faster performance
  - No downtime

### 🚀 Production Optimizations

1. **Upgrade to Paid Plan** for production use
2. **Add Custom Domain** in Render dashboard
3. **Configure Environment-Specific Settings**
4. **Set up Monitoring** and alerts
5. **Add Database** if needed for user data

### ✅ Success Checklist

- [ ] Code pushed to GitHub
- [ ] Render service created and deployed
- [ ] Health check endpoint responding
- [ ] API endpoints working correctly
- [ ] Judge0 integration functioning
- [ ] Environment variables configured
- [ ] Logs showing successful startup

### 📞 Support

If you encounter issues:

1. **Check Render Logs** for error details
2. **Test Locally** to isolate issues
3. **Review Documentation** at [render.com/docs](https://render.com/docs)
4. **Check Judge0 Status** if execution fails

---

## 🎉 Your API is Live!

Once deployed, your EduRun AI Code Buddy backend will be accessible globally with:

- ✅ Multi-language code execution via Judge0
- ✅ REST API endpoints
- ✅ Health monitoring
- ✅ Automatic HTTPS
- ✅ Continuous deployment

**Example Frontend Integration:**
```javascript
const API_URL = 'https://your-service-name.onrender.com';

// Execute code
const response = await fetch(`${API_URL}/api/compile`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: 'print("Hello from Render!")',
    language: 'python'
  })
});

const result = await response.json();
console.log(result.output);
```

Happy coding! 🚀
