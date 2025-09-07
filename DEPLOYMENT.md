# 🚀 CropLeaf Deployment Guide

## Overview
This guide will help you deploy the CropLeaf application using **Vercel** (Frontend) and **Railway** (Backend) - both offer generous free tiers!

## Prerequisites
- GitHub account
- Railway account (https://railway.app)
- Vercel account (https://vercel.com)

---

## Step 1: Backend Deployment (Railway)

### 1.1 Create Railway Project
1. Go to [Railway.app](https://railway.app) and sign up/login
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub account and select this repository
4. Railway will automatically detect it's a Python/Django project

### 1.2 Set up PostgreSQL Database
1. In your Railway project, go to "Variables" tab
2. Add these environment variables:
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=your-railway-domain.up.railway.app
DB_NAME=postgresql
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=containers-us-west-1.railway.app
DB_PORT=5432
DB_SSL=true
```

### 1.3 Deploy Backend
1. Railway will automatically deploy your backend
2. Once deployed, copy the backend URL (something like: `https://crop-leaf-backend.up.railway.app`)

---

## Step 2: Frontend Deployment (Vercel)

### 2.1 Create Vercel Project
1. Go to [Vercel.com](https://vercel.com) and sign up/login
2. Click "New Project" → "Import Git Repository"
3. Connect your GitHub account and select this repository
4. Configure the project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 2.2 Set Environment Variables
1. In Vercel project settings, go to "Environment Variables"
2. Add this variable:
```
VITE_API_URL=https://your-railway-backend-url.up.railway.app
```

### 2.3 Deploy Frontend
1. Click "Deploy"
2. Vercel will build and deploy your frontend
3. Once deployed, you'll get a URL like: `https://crop-leaf.vercel.app`

---

## Step 3: Final Configuration

### 3.1 Update CORS Settings
In your Railway backend, update the `ALLOWED_HOSTS` and CORS settings:
```python
ALLOWED_HOSTS = ['your-vercel-domain.vercel.app', 'localhost', '127.0.0.1']
CORS_ALLOWED_ORIGINS = [
    'https://your-vercel-domain.vercel.app',
    'http://localhost:3000',
    'http://localhost:5173',
]
```

### 3.2 Test the Deployment
1. Visit your Vercel frontend URL
2. Try uploading an image for disease prediction
3. Check if the API calls work properly

---

## Troubleshooting

### Backend Issues:
- Check Railway logs for any errors
- Ensure all environment variables are set correctly
- Make sure the database is connected

### Frontend Issues:
- Check Vercel build logs
- Ensure VITE_API_URL is set correctly
- Check browser console for CORS errors

### Common Issues:
- **CORS errors**: Update CORS_ALLOWED_ORIGINS in Django settings
- **Database connection**: Verify Railway PostgreSQL credentials
- **Static files**: WhiteNoise should handle this automatically

---

## Cost Breakdown (Free Tiers)

### Railway (Backend):
- 512MB RAM, 1GB Disk
- PostgreSQL database included
- 100 hours/month free

### Vercel (Frontend):
- Unlimited static sites
- 100GB bandwidth/month
- Custom domains free

---

## Need Help?
If you encounter any issues during deployment, check:
1. Railway/Vercel deployment logs
2. Environment variables are set correctly
3. Database connections are working
4. CORS settings match your domains

Happy deploying! 🌾🚀