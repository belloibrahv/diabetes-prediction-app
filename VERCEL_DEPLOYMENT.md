# Vercel Deployment Guide for Diabetes Prediction App

## 🚀 Deployment Status: READY ✅

### Latest Changes Made:
- ✅ Optimized `requirements.txt` for Vercel (removed ML training dependencies)
- ✅ Created `vercel.json` configuration
- ✅ Created `.vercelignore` file
- ✅ Kept only essential dependencies (Flask, numpy, joblib, python-dotenv)

## 📋 Current Configuration Files

### `requirements.txt` (Optimized for Vercel)
```
Flask==3.0.0
Werkzeug==3.0.1
numpy==2.3.1
joblib==1.4.2
python-dotenv==1.0.0
```

### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  },
  "functions": {
    "app.py": {
      "maxDuration": 30
    }
  }
}
```

### `.vercelignore`
```
# Excludes unnecessary files from deployment
# Python cache, docs, data files, etc.
```

## 🔧 Deployment Steps

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy to Vercel
```bash
# From your project directory
vercel

# Or for production deployment
vercel --prod
```

### 4. Alternative: Deploy via GitHub Integration
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository: `belloibrahv/diabetes-prediction-app`
4. Configure settings:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave empty)
   - **Build Command**: Leave empty (Vercel auto-detects)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

## 📚 Official Vercel Documentation References

### Flask Deployment
- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Flask on Vercel](https://vercel.com/guides/deploying-flask-with-vercel)
- [Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

### Configuration
- [vercel.json Reference](https://vercel.com/docs/projects/project-configuration)
- [Environment Variables](https://vercel.com/docs/projects/environment-variables)
- [Function Configuration](https://vercel.com/docs/functions/serverless-functions/runtimes/python#function-configuration)

### Troubleshooting
- [Vercel Debugging](https://vercel.com/docs/debugging)
- [Function Logs](https://vercel.com/docs/functions/serverless-functions/runtimes/python#function-logs)
- [Common Issues](https://vercel.com/docs/debugging#common-issues)

## 🐛 Common Issues & Solutions

### Issue 1: Model Loading in Serverless Environment
**Error**: `FileNotFoundError: models/model.pkl`

**Solution**:
- ✅ Model files are included in deployment
- ✅ Using relative paths in app.py
- ✅ Models are in `models/` directory

### Issue 2: Function Timeout
**Error**: Function execution timeout

**Solution**:
- ✅ Set `maxDuration: 30` in vercel.json
- ✅ Optimized model loading
- ✅ Efficient prediction logic

### Issue 3: Static Files Not Loading
**Error**: CSS/JS files not found

**Solution**:
- ✅ Added static file route in vercel.json
- ✅ Static files in correct directory structure

### Issue 4: Import Errors
**Error**: `ModuleNotFoundError`

**Solution**:
- ✅ Only essential dependencies in requirements.txt
- ✅ Removed ML training dependencies (pandas, scikit-learn)
- ✅ Kept only runtime dependencies

## 🔍 Debugging Commands

### Local Testing
```bash
# Test requirements installation
pip install -r requirements.txt

# Test Flask app locally
python app.py

# Test Vercel build locally
vercel dev
```

### Vercel Logs
```bash
# View deployment logs
vercel logs

# View function logs
vercel logs --function app.py
```

## 📊 Health Check Endpoints

Your app includes these endpoints for monitoring:
- `/health` - Basic health check
- `/` - Main application
- `/predict` - Prediction endpoint
- `/api/predict` - API endpoint

## 🎯 Vercel-Specific Optimizations

### 1. Serverless Function Optimization
- ✅ Model loading at startup (cold start optimization)
- ✅ Efficient memory usage
- ✅ Quick response times

### 2. Static File Handling
- ✅ CSS and JS files served efficiently
- ✅ Proper routing configuration
- ✅ CDN optimization

### 3. Environment Variables
- ✅ Production environment set
- ✅ Secure configuration
- ✅ No sensitive data in code

### 4. Function Limits
- ✅ Under 50MB function size
- ✅ Under 30-second execution time
- ✅ Efficient model inference

## 🚨 Emergency Rollback

If deployment fails:
1. Check Vercel logs for specific errors
2. Revert to previous working commit
3. Test locally with `vercel dev`
4. Update configuration if needed

## 📞 Support Resources

- [Vercel Support](https://vercel.com/support)
- [Vercel Community](https://github.com/vercel/vercel/discussions)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python on Vercel](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

## ✅ Deployment Checklist

- [ ] All files committed to GitHub
- [ ] requirements.txt optimized for Vercel
- [ ] vercel.json configured correctly
- [ ] .vercelignore excludes unnecessary files
- [ ] Model files in models/ directory
- [ ] Local testing passes
- [ ] Vercel CLI installed and logged in
- [ ] Deployment command executed
- [ ] App accessible via Vercel URL
- [ ] Health check endpoint responds
- [ ] Prediction form loads correctly

## 🎉 Success Indicators

When deployment is successful, you should see:
- ✅ Build status: "Ready"
- ✅ Function status: "Active"
- ✅ App accessible at: `https://your-app-name.vercel.app`
- ✅ Health check endpoint responds
- ✅ Prediction form loads correctly
- ✅ Static files (CSS) load properly

## 🔄 Continuous Deployment

Vercel automatically deploys when you push to GitHub:
1. Push changes to `main` branch
2. Vercel automatically detects changes
3. Builds and deploys automatically
4. Preview deployments for pull requests

---

**Last Updated**: December 2024
**Status**: Ready for Vercel Deployment ✅ 