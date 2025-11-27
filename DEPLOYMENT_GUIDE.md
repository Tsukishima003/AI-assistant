# 🚀 Deployment Guide - RAG Chat Application

## 📋 Overview

Your application consists of:
- **Frontend**: React + Vite (currently on `localhost:3000`)
- **Backend**: FastAPI + Python (currently on `localhost:8000`)
- **Database**: ChromaDB Cloud (already hosted)

---

## 🎯 Deployment Options

### Option 1: Vercel (Frontend) + Render/Railway (Backend) ⭐ **Recommended**
### Option 2: Full Stack on Railway
### Option 3: Docker + Any Cloud Platform
### Option 4: Traditional VPS (DigitalOcean, AWS, etc.)

---

## ✅ Option 1: Vercel + Render (Easiest & Free Tier Available)

### **Frontend Deployment (Vercel)**

#### **Step 1: Prepare Frontend for Production**

Create `frontend/.env.production`:
```env
VITE_API_URL=https://your-backend.onrender.com
VITE_WS_URL=wss://your-backend.onrender.com/ws/chat
```

Update `frontend/src/config/constants.js`:
```javascript
// Use environment variables for production
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/chat';
```

#### **Step 2: Deploy to Vercel**

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy (from frontend directory)
cd frontend
vercel

# For production deployment
vercel --prod
```

**Or use Vercel Dashboard:**
1. Go to https://vercel.com
2. Import your GitHub repo
3. Set root directory to `frontend`
4. Add environment variables
5. Deploy!

---

### **Backend Deployment (Render.com)**

#### **Step 1: Create `requirements.txt`**

```bash
cd backend
pip freeze > requirements.txt
```

#### **Step 2: Create `render.yaml`** (optional but recommended)

```yaml
services:
  - type: web
    name: rag-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m app.main
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: GROQ_API_KEY
        sync: false
      - key: CHROMA_USE_CLOUD
        value: true
      - key: CHROMA_CLOUD_API_KEY
        sync: false
      - key: CHROMA_CLOUD_TENANT
        sync: false
      - key: CHROMA_CLOUD_DATABASE
        value: RAG
      - key: HOST
        value: 0.0.0.0
      - key: PORT
        value: 8000
```

#### **Step 3: Deploy on Render**

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Name**: `rag-backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m app.main`
   - **Instance Type**: Free tier
5. Add environment variables (from `.env`)
6. Deploy!

---

## ✅ Option 2: Railway (Full Stack Deployment)

Railway can host both frontend and backend easily.

### **Step 1: Prepare Project**

Create `railway.json` in project root:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### **Step 2: Deploy**

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy backend
cd backend
railway up

# Deploy frontend (in another service)
cd ../frontend
railway up
```

**Or use Railway Dashboard:**
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Add two services:
   - Backend (root: `backend`, start: `python -m app.main`)
   - Frontend (root: `frontend`, start: `npm run build && npm run preview`)
4. Set environment variables
5. Deploy!

---

## ✅ Option 3: Docker Deployment

### **Create `backend/Dockerfile`:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "-m", "app.main"]
```

### **Create `frontend/Dockerfile`:**

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy and build
COPY . .
RUN npm run build

# Production image
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### **Create `frontend/nginx.conf`:**

```nginx
server {
    listen 80;
    server_name _;
    
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
}
```

### **Create `docker-compose.yml`:**

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - CHROMA_USE_CLOUD=true
      - CHROMA_CLOUD_API_KEY=${CHROMA_CLOUD_API_KEY}
      - CHROMA_CLOUD_TENANT=${CHROMA_CLOUD_TENANT}
      - CHROMA_CLOUD_DATABASE=RAG
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

**Deploy:**
```bash
docker-compose up -d
```

---

## ✅ Option 4: Traditional VPS (DigitalOcean, AWS, etc.)

### **Backend Setup**

```bash
# SSH into your server
ssh user@your-server-ip

# Install Python
sudo apt update
sudo apt install python3.11 python3-pip

# Clone your repo
git clone your-repo-url
cd your-repo/backend

# Install dependencies
pip3 install -r requirements.txt

# Create .env file
nano .env
# Add your environment variables

# Run with screen or tmux
screen -S backend
python3 -m app.main

# Or use systemd service (better)
sudo nano /etc/systemd/system/rag-backend.service
```

**Systemd service file:**
```ini
[Unit]
Description=RAG Backend API
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/backend
Environment="PATH=/usr/bin"
ExecStart=/usr/bin/python3 -m app.main
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable rag-backend
sudo systemctl start rag-backend
```

### **Frontend Setup**

```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs

# Build frontend
cd ../frontend
npm install
npm run build

# Serve with nginx
sudo apt install nginx
sudo cp dist/* /var/www/html/
sudo systemctl restart nginx
```

---

## 🔒 Environment Variables Setup

### **Backend (.env)**

```env
GROQ_API_KEY=your_actual_groq_key
CHROMA_USE_CLOUD=true
CHROMA_CLOUD_API_KEY=ck-JwTn7mhwCpAx3mR8wP-tQE133vRUFW6PRwulqWR87
CHROMA_CLOUD_TENANT=3adc1fd1-1bd8-4588-9321-2977f78c9880
CHROMA_CLOUD_DATABASE=RAG
HOST=0.0.0.0
PORT=8000
GROQ_MODEL=llama-3.1-70b-versatile
```

### **Frontend (.env.production)**

```env
VITE_API_URL=https://your-backend-url.com
VITE_WS_URL=wss://your-backend-url.com/ws/chat
```

---

## 📝 Pre-Deployment Checklist

### **Backend:**
- [ ] Create `requirements.txt`: `pip freeze > requirements.txt`
- [ ] Test production mode locally
- [ ] Set all environment variables
- [ ] Verify ChromaDB Cloud connection
- [ ] Update CORS settings for production domain

### **Frontend:**
- [ ] Update API URLs for production
- [ ] Build and test: `npm run build && npm run preview`
- [ ] Optimize images/assets
- [ ] Set environment variables

### **General:**
- [ ] Get domain name (optional)
- [ ] Set up SSL certificates
- [ ] Configure monitoring
- [ ] Set up backups

---

## 🎯 Recommended Quick Start: Vercel + Render

**Why?**
- ✅ Free tiers available
- ✅ Automatic HTTPS
- ✅ Easy CI/CD with GitHub
- ✅ Good performance
- ✅ Simple setup

**Time to deploy: ~30 minutes**

### **Quick Steps:**

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-github-repo
   git push -u origin main
   ```

2. **Deploy Backend (Render)**
   - Go to render.com → New Web Service
   - Connect GitHub
   - Root: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `python -m app.main`
   - Add env vars
   - Deploy!

3. **Deploy Frontend (Vercel)**
   - Go to vercel.com → New Project
   - Import from GitHub
   - Root: `frontend`
   - Framework: Vite
   - Add env vars (with backend URL)
   - Deploy!

4. **Update Frontend to use Backend URL**
   - Get Render backend URL
   - Add to Vercel environment variables
   - Redeploy

**Done! Your app is live! 🎉**

---

## 🔍 Post-Deployment

### **Monitor Your App:**
- Check logs in Render/Vercel dashboard
- Set up error tracking (e.g., Sentry)
- Monitor API usage (Groq dashboard)

### **Custom Domain:**
- Buy domain (Namecheap, Google Domains)
- Add to Vercel: Settings → Domains
- Update CORS in backend for new domain

### **SSL/HTTPS:**
- Automatic on Vercel
- Automatic on Render
- Use Let's Encrypt for VPS

---

## 🆘 Troubleshooting

### **CORS Errors:**
Update `backend/app/config/cors.py`:
```python
allow_origins=["https://your-frontend-domain.vercel.app"]
```

### **WebSocket Not Connecting:**
- Make sure using `wss://` not `ws://` for HTTPS
- Check firewall settings
- Verify WebSocket support on platform

### **Build Fails:**
- Check Python/Node version
- Verify all dependencies in requirements.txt/package.json
- Check build logs for specific errors

---

## 📚 Resources

- [Vercel Docs](https://vercel.com/docs)
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html)

---

**Ready to deploy? Start with Vercel + Render for the easiest experience!** 🚀
