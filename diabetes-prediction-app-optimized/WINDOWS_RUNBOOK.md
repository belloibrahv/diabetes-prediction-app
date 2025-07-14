# DIABETES PREDICTION APP - WINDOWS RUNBOOK
## Complete Setup and Running Guide for Windows Systems

---

## 📋 **PREREQUISITES**

### **Required Software:**
1. **Python 3.8 or higher** - Download from [python.org](https://www.python.org/downloads/)
2. **Git** (optional) - Download from [git-scm.com](https://git-scm.com/download/win)
3. **Text Editor** - VS Code, Notepad++, or any text editor

### **System Requirements:**
- Windows 10 or higher
- At least 4GB RAM
- 2GB free disk space
- Internet connection for package installation

---

## 🚀 **STEP-BY-STEP SETUP**

### **Step 1: Verify Python Installation**
```cmd
# Open Command Prompt and run:
python --version
# Should show Python 3.8.x or higher

# Also check pip:
pip --version
```

**If Python is not installed:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python version for Windows
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Restart Command Prompt after installation

### **Step 2: Create Project Directory**
```cmd
# Navigate to your desired location (e.g., Desktop)
cd C:\Users\YourUsername\Desktop

# Create project folder
mkdir diabetes-prediction-app
cd diabetes-prediction-app
```

### **Step 3: Extract Project Files**
1. Extract the `diabetes-prediction-app-optimized.zip` file
2. Copy all contents to your project directory
3. Verify the following structure:
```
diabetes-prediction-app/
├── app.py
├── requirements.txt
├── README.md
├── models/
│   ├── model.pkl
│   ├── scaler.pkl
│   ├── feature_names.pkl
│   └── label_encoders.pkl
├── templates/
│   └── index.html
└── static/
    └── css/
        └── style.css
```

### **Step 4: Create Virtual Environment**
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) at the beginning of your command line
```

### **Step 5: Install Dependencies**
```cmd
# Make sure virtual environment is activated (venv)
pip install -r requirements.txt
```

**Expected output:** All packages will be installed successfully

### **Step 6: Verify Installation**
```cmd
# Check if Flask is installed
python -c "import flask; print('Flask installed successfully')"

# Check if other key packages are available
python -c "import pickle, numpy, joblib; print('All packages ready')"
```

---

## 🏃‍♂️ **RUNNING THE APPLICATION**

### **Method 1: Development Mode (Recommended for testing)**
```cmd
# Make sure you're in the project directory and virtual environment is activated
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### **Method 2: Production Mode**
```cmd
# Set environment variable for production
set FLASK_ENV=production
python app.py
```

---

## 🌐 **ACCESSING THE APPLICATION**

### **Local Access:**
1. Open your web browser
2. Go to: `http://127.0.0.1:5000` or `http://localhost:5000`
3. You should see the Diabetes Prediction interface

### **Network Access (for other devices on same network):**
```cmd
# Run with host parameter
python app.py --host=0.0.0.0
```
Then access via: `http://YOUR_COMPUTER_IP:5000`

---

## 🧪 **TESTING THE APPLICATION**

### **Sample Test Data:**
Use these values to test the prediction:
- **Age:** 35
- **Gender:** Male
- **BMI:** 25.5
- **Blood Pressure:** 120/80
- **Glucose Level:** 140
- **Insulin Level:** 80
- **Diabetes Pedigree Function:** 0.5

### **Expected Results:**
- System should process the data
- Show prediction result (High Risk/Low Risk)
- Display confidence percentage
- Provide treatment recommendations

---

## 🔧 **TROUBLESHOOTING**

### **Common Issues and Solutions:**

#### **Issue 1: "python is not recognized"**
**Solution:**
```cmd
# Check if Python is in PATH
where python
# If not found, reinstall Python with "Add to PATH" checked
```

#### **Issue 2: "pip is not recognized"**
**Solution:**
```cmd
# Try using python -m pip instead
python -m pip install -r requirements.txt
```

#### **Issue 3: "ModuleNotFoundError"**
**Solution:**
```cmd
# Make sure virtual environment is activated
venv\Scripts\activate
# Reinstall requirements
pip install -r requirements.txt
```

#### **Issue 4: "Port 5000 already in use"**
**Solution:**
```cmd
# Kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
# Or use a different port
python app.py --port=5001
```

#### **Issue 5: "Model files not found"**
**Solution:**
```cmd
# Check if model files exist
dir models
# Should show: model.pkl, scaler.pkl, feature_names.pkl, label_encoders.pkl
```

---

## 📁 **PROJECT STRUCTURE EXPLANATION**

### **Core Files:**
- **`app.py`** - Main Flask application with all routes and logic
- **`requirements.txt`** - Python package dependencies
- **`README.md`** - Project documentation

### **Model Files:**
- **`models/model.pkl`** - Trained machine learning model
- **`models/scaler.pkl`** - Data normalization scaler
- **`models/feature_names.pkl`** - Feature names for input validation
- **`models/label_encoders.pkl`** - Categorical data encoders

### **Web Interface:**
- **`templates/index.html`** - Main web page template
- **`static/css/style.css`** - Styling for the web interface

---

## 🔒 **SECURITY CONSIDERATIONS**

### **For Development:**
- Application runs on localhost only
- No external access by default
- Debug mode enabled for development

### **For Production:**
- Disable debug mode
- Use proper WSGI server (Gunicorn, uWSGI)
- Configure firewall rules
- Use HTTPS for sensitive data

---

## 📊 **PERFORMANCE MONITORING**

### **Check Application Status:**
```cmd
# Check if app is running
netstat -ano | findstr :5000

# Monitor CPU and memory usage
tasklist | findstr python
```

### **Logs:**
- Application logs appear in the command prompt
- Check for error messages in the console output

---

## 🚀 **DEPLOYMENT OPTIONS**

### **Local Network Deployment:**
```cmd
# Allow external access
python app.py --host=0.0.0.0 --port=5000
```

### **Cloud Deployment:**
- **Heroku:** Use Procfile and requirements.txt
- **Vercel:** Use vercel.json configuration
- **Render:** Use render.yaml configuration

---

## 📞 **SUPPORT**

### **If you encounter issues:**
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure virtual environment is activated
4. Check that all model files are present
5. Review console output for error messages

### **Contact Information:**
- **Project Repository:** [GitHub Link]
- **Documentation:** See README.md for detailed information

---

## ✅ **VERIFICATION CHECKLIST**

- [ ] Python 3.8+ installed and in PATH
- [ ] Virtual environment created and activated
- [ ] All dependencies installed successfully
- [ ] Model files present in models/ directory
- [ ] Application starts without errors
- [ ] Web interface accessible at localhost:5000
- [ ] Prediction functionality working
- [ ] Sample data test successful

**🎉 Congratulations! Your Diabetes Prediction App is now running successfully on Windows!** 