# Quick Vercel Deployment Guide

## 🚀 Fast Deployment Steps

### Option 1: Using Deployment Script
```bash
./deploy.sh
```

### Option 2: Manual Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Option 3: GitHub Integration
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import: `belloibrahv/diabetes-prediction-app`
4. Deploy!

## 📋 What's Configured

✅ **requirements.txt** - Only essential dependencies
✅ **vercel.json** - Flask configuration
✅ **.vercelignore** - Excludes unnecessary files
✅ **Model files** - Ready for serverless environment
✅ **Static files** - CSS properly configured

## 🔧 Key Optimizations

- **Dependencies**: Removed pandas, scikit-learn (not needed for inference)
- **Model Loading**: Optimized for serverless cold starts
- **Static Files**: Proper routing for CSS/JS
- **Function Limits**: 30-second timeout configured

## 🎯 Expected Result

After deployment, you'll get:
- ✅ Live URL: `https://your-app-name.vercel.app`
- ✅ Health check: `/health` endpoint
- ✅ Prediction form: Working diabetes assessment
- ✅ API endpoint: `/api/predict` for programmatic access

## 🚨 If Issues Occur

1. Check logs: `vercel logs`
2. Test locally: `vercel dev`
3. Verify model files are in `models/` directory
4. Ensure all files are committed to GitHub

---

**Status**: Ready for deployment! 🚀 