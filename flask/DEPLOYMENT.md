# Diabetes Prediction App - Vercel Deployment Guide

## Prerequisites

1. **Node.js and npm** - Required for Vercel CLI
2. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
3. **Git Repository** - Your project should be in a Git repository

## Deployment Steps

### Method 1: Using Vercel CLI (Recommended)

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Navigate to the flask directory**:
   ```bash
   cd flask
   ```

3. **Run the deployment script**:
   ```bash
   ./deploy.sh
   ```

   Or manually deploy:
   ```bash
   vercel --prod
   ```

### Method 2: Using Vercel Dashboard

1. **Push your code to GitHub/GitLab/Bitbucket**

2. **Connect your repository to Vercel**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your Git repository
   - Set the root directory to `flask`
   - Deploy

### Method 3: Manual Deployment

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   cd flask
   vercel --prod
   ```

## Configuration Files

### vercel.json
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
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### requirements.txt
Contains all Python dependencies needed for the Flask application.

## Environment Variables

The following environment variables are automatically handled:
- `FLASK_ENV`: Set to "production" by Vercel
- `PORT`: Automatically set by Vercel

## Troubleshooting

### Common Issues

1. **Model files not found**:
   - Ensure all `.pkl` files are in the flask directory
   - Check file permissions

2. **Import errors**:
   - Verify all dependencies are in `requirements.txt`
   - Check Python version compatibility

3. **Build failures**:
   - Check Vercel build logs
   - Ensure all required files are present

### Debugging

1. **Check build logs**:
   - Go to your Vercel dashboard
   - Click on the latest deployment
   - View build logs for errors

2. **Test locally**:
   ```bash
   cd flask
   python app.py
   ```

3. **Check health endpoint**:
   - Visit `https://your-app.vercel.app/health`
   - Should return JSON with status information

## Post-Deployment

1. **Test your application**:
   - Visit your deployed URL
   - Test the prediction functionality
   - Check all features work correctly

2. **Monitor performance**:
   - Use Vercel Analytics
   - Monitor error rates
   - Check response times

3. **Set up custom domain** (optional):
   - Go to Vercel dashboard
   - Add custom domain
   - Configure DNS settings

## File Structure

```
flask/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
├── model.pkl            # Trained ML model
├── scaler.pkl           # Feature scaler
├── label_encoders.pkl   # Label encoders
├── feature_names.pkl    # Feature names
├── deploy.sh            # Deployment script
├── DEPLOYMENT.md        # This file
├── static/              # Static files (CSS, JS)
└── templates/           # HTML templates
```

## Support

If you encounter issues:
1. Check the Vercel documentation
2. Review build logs in Vercel dashboard
3. Test locally first
4. Ensure all files are properly committed to Git 