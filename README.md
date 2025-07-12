# Diabetes Prediction AI Application

A comprehensive Flask-based web application for diabetes prediction using machine learning. This application provides risk assessment, personalized recommendations, and educational content for diabetes management.

## 🏗️ Project Structure

```
Diabetes-Prediction/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment configuration
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
    ├── diabetes.ipynb   # Jupyter notebook
    ├── merge_diabetes_data.py # Data processing script
    └── ...              # Other documentation files
```

## 🚀 Features

### Core Functionality
- **Advanced Diabetes Prediction**: ML-powered risk assessment
- **Risk Stratification**: High, Moderate, Low, Very Low risk levels
- **Diabetes Type Classification**: Type 1, Type 2, or No Diabetes
- **Personalized Recommendations**: Evidence-based treatment suggestions
- **Educational Content**: Comprehensive diabetes education
- **Data Export**: CSV report generation
- **Responsive UI**: Modern, mobile-friendly interface

### Technical Features
- **Machine Learning Model**: Gradient Boosting Classifier (95.5% accuracy)
- **Feature Engineering**: Comprehensive data preprocessing
- **API Endpoints**: RESTful API for integration
- **Health Monitoring**: Built-in health check endpoints
- **Error Handling**: Robust error management
- **Logging**: Comprehensive application logging

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Machine Learning**: scikit-learn, pandas, numpy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Deployment**: Render (Cloud Platform)
- **Version Control**: Git, GitHub

## 📊 Model Performance

- **Accuracy**: 95.5%
- **Most Important Features**: HbA1c, Age, BMI, Gender
- **Model Type**: Gradient Boosting Classifier
- **Validation**: Cross-validation and ROC analysis

## 🚀 Deployment

### Render Deployment

This application is optimized for deployment on Render.com:

1. **Fork/Clone** this repository
2. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repository
   - Set Root Directory to `/` (root of this project)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
3. **Deploy** and get your live URL

### Local Development

```bash
# Clone the repository
git clone https://github.com/belloibrahv/diabetes-prediction-app.git
cd diabetes-prediction-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access at http://localhost:5050
```

## 📋 API Endpoints

### Web Interface
- `GET /` - Main application interface
- `POST /predict` - Form-based prediction
- `GET /health` - Health check endpoint

### REST API
- `POST /api/predict` - JSON-based prediction
- `POST /export-report` - Export prediction report as CSV

### Example API Usage

```bash
curl -X POST https://your-app.onrender.com/api/predict \
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

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `production` for deployment
- `SECRET_KEY`: Flask secret key (auto-generated if not set)

### Model Configuration
- Model files are stored in `models/` directory
- Automatic model loading on application startup
- Fallback handling for missing model files

## 📈 Model Training

The ML model was trained on a comprehensive dataset with the following features:
- Age, Gender, BMI, Weight, Height
- HbA1c, Physical Activity, Dietary Habits
- Family History, Existing Conditions
- Hypertension, Heart Disease, Smoking History

**Note**: Insulin and Glucose parameters were intentionally excluded as per research requirements to maintain the predictive nature of the system.

## 🎯 Functional Requirements Met

✅ **Comprehensive Data Input**: All required parameters included
✅ **Advanced Diabetes Prediction**: Risk classification and type detection
✅ **Comprehensive Results Display**: Detailed risk assessment and recommendations
✅ **Evidence-based Treatment Recommendations**: Personalized medical advice
✅ **Educational Content**: Comprehensive diabetes education
✅ **Data Export/Sharing**: CSV report generation
✅ **Responsive UI**: Modern, intuitive interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation in `docs/`
2. Review the API endpoints
3. Test the health endpoint: `/health`
4. Contact the development team

## 🔗 Live Application

**Deployed on Render**: [Your Render URL will appear here after deployment]

---

**Built with ❤️ for diabetes care and prevention**
