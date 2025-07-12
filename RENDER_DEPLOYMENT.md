# Render Deployment Guide for Diabetes Prediction App

This guide follows the official Render documentation for deploying ML-driven Flask applications.

## 🚀 Prerequisites

- GitHub repository with your code
- Render account (free tier available)
- Python 3.11+ compatibility

## 📁 Project Structure (Optimized for Render)

```
diabetes-prediction-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Render process configuration
├── runtime.txt           # Python version specification
├── models/               # ML model files
│   ├── model.pkl        # Trained ML model
│   ├── scaler.pkl       # Feature scaler
│   ├── label_encoders.pkl # Label encoders
│   └── feature_names.pkl # Feature names
├── static/               # Static files
│   └── css/
│       └── style.css    # Application styles
├── templates/            # HTML templates
│   └── index.html       # Main application template
└── docs/                # Documentation and assets
```

## 🛠️ Deployment Steps

### Step 1: Prepare Your Repository

✅ **Already Done**: Your repository is properly organized with:
- Clean project structure
- All model files in `models/` directory
- Proper `requirements.txt` with compatible versions
- `Procfile` for Render deployment
- `runtime.txt` specifying Python 3.11

### Step 2: Deploy to Render

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Sign in or create account

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"

3. **Connect GitHub Repository**
   - Click "Connect" next to GitHub
   - Authorize Render to access your repositories
   - Select `belloibrahv/diabetes-prediction-app`

4. **Configure the Service**
   - **Name**: `diabetes-prediction-app` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty (uses repository root)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

5. **Advanced Settings (Optional)**
   - **Auto-Deploy**: Enabled (recommended)
   - **Health Check Path**: `/health`

6. **Environment Variables (Optional)**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   ```

7. **Click "Create Web Service"**

### Step 3: Monitor Deployment

1. **Build Process**
   - Render will install dependencies from `requirements.txt`
   - Build time: ~2-3 minutes
   - Watch the build logs for any errors

2. **Startup Process**
   - Gunicorn will start the Flask application
   - Health check will verify `/health` endpoint
   - Service becomes available at provided URL

## 🔧 Configuration Files Explained

### `requirements.txt`
```txt
Flask==3.0.0
Werkzeug==3.0.1
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
gunicorn==21.2.0
python-dotenv==1.0.0
flask-cors==4.0.0
```

### `Procfile`
```txt
web: gunicorn app:app
```
- Tells Render how to start the application
- Uses Gunicorn WSGI server for production

### `runtime.txt`
```txt
python-3.11
```
- Specifies Python version for Render
- Ensures compatibility with ML libraries

## 🧪 Testing Your Deployment

### Health Check
```bash
curl https://your-app-name.onrender.com/health
```
Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "scaler_loaded": true,
  "encoders_loaded": true,
  "timestamp": "2025-07-12T..."
}
```

### API Testing
```bash
curl -X POST https://your-app-name.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 45,
    "Gender": "Male",
    "BMI": 28.5,
    "HbA1c": 6.2,
    "Hypertension": 1,
    "HeartDisease": 0,
    "SmokingHistory": "former"
  }'
```

## 🔍 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check `requirements.txt` for compatible versions
   - Ensure all dependencies are listed
   - Verify Python version in `runtime.txt`

2. **Model Loading Errors**
   - Verify model files are in `models/` directory
   - Check file permissions
   - Ensure model files are committed to Git

3. **Startup Failures**
   - Check `Procfile` syntax
   - Verify `app.py` exists and is properly configured
   - Review build logs for errors

4. **Health Check Failures**
   - Ensure `/health` endpoint is implemented
   - Check application logs for errors
   - Verify all model files are accessible

### Debugging Commands

```bash
# Check application logs
# Available in Render dashboard under "Logs" tab

# Test local deployment
python app.py

# Test with gunicorn locally
gunicorn app:app

# Check model loading
python -c "import pickle; pickle.load(open('models/model.pkl', 'rb'))"
```

## 📊 Performance Optimization

### Render Free Tier Limits
- **Build Time**: 15 minutes
- **Request Timeout**: 30 seconds
- **Memory**: 512 MB
- **Sleep**: Services sleep after 15 minutes of inactivity

### Optimization Tips
1. **Model Size**: Keep models under 100MB
2. **Dependencies**: Use specific versions in `requirements.txt`
3. **Cold Start**: First request may take 10-30 seconds
4. **Caching**: Implement response caching for predictions

## 🔄 Continuous Deployment

### Auto-Deploy Setup
1. **Enable Auto-Deploy** in Render dashboard
2. **Push to main branch** triggers automatic deployment
3. **Monitor deployment** in Render dashboard

### Manual Deployment
1. **Trigger Manual Deploy** in Render dashboard
2. **Select branch** to deploy
3. **Monitor build** and startup process

## 📈 Monitoring and Analytics

### Render Dashboard Features
- **Real-time logs**: Monitor application performance
- **Metrics**: Request count, response times
- **Alerts**: Set up notifications for failures
- **Scaling**: Upgrade plan for higher traffic

### Health Monitoring
- **Automatic health checks** every 30 seconds
- **Custom health endpoint** at `/health`
- **Model status** included in health response

## 🚀 Post-Deployment

### Update Your README
```markdown
## 🔗 Live Application

**Deployed on Render**: https://your-app-name.onrender.com

- **Health Check**: https://your-app-name.onrender.com/health
- **API Documentation**: See README.md for endpoints
```

### Share Your Application
- **Public URL**: Share with users and stakeholders
- **API Access**: Provide API documentation
- **GitHub**: Link to source code repository

## 🎯 Success Checklist

- [ ] Repository properly organized
- [ ] All model files in `models/` directory
- [ ] `requirements.txt` with compatible versions
- [ ] `Procfile` configured for gunicorn
- [ ] `runtime.txt` specifies Python 3.11
- [ ] Health endpoint `/health` working
- [ ] API endpoints responding correctly
- [ ] Application accessible via public URL
- [ ] Auto-deploy enabled for future updates

## 📞 Support

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **GitHub Issues**: Report bugs in repository
- **Render Support**: Available in dashboard

---

**Your diabetes prediction app is now ready for professional deployment on Render!** 🎉 