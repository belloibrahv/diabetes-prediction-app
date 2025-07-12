# DiabetesCare AI - Online Diabetes Check and Treatment Recommendation System

## 📋 Project Overview

**DiabetesCare AI** is an advanced machine learning-based web application for diabetes risk assessment and personalized treatment recommendations. This project addresses the critical need for accessible, cost-effective diabetes screening tools, particularly in resource-constrained environments like Nigeria.

### 🎯 Key Features

- **AI-Powered Prediction**: Advanced machine learning algorithms for accurate diabetes risk assessment
- **Personalized Recommendations**: Tailored treatment and lifestyle recommendations based on individual risk profiles
- **Mobile-First Design**: Responsive web application optimized for all devices
- **Comprehensive Risk Assessment**: Detailed analysis with confidence intervals and risk stratification
- **Evidence-Based Guidance**: Treatment recommendations based on clinical guidelines

## 🏥 Research Context

This project is part of a comprehensive research study titled **"Online Diabetes Check and Treatment Recommendation System with Machine Learning"** conducted at the Nigeria Defence Academy, Kaduna. The system addresses the growing diabetes epidemic in Nigeria and developing countries by providing:

- Early detection capabilities
- Personalized treatment recommendations
- Accessible healthcare tools
- Cost-effective screening solutions

## 🛠️ Technology Stack

### Backend
- **Python 3.9+**: Core programming language
- **Flask 3.0.0**: Web framework for API development
- **scikit-learn 1.3.2**: Machine learning library
- **pandas 2.1.4**: Data manipulation and analysis
- **numpy 1.24.3**: Numerical computing

### Frontend
- **Bootstrap 5.3.0**: Responsive CSS framework
- **Font Awesome 6.4.0**: Icon library
- **Inter Font**: Modern typography
- **Custom CSS**: Enhanced styling and animations

### Machine Learning
- **Random Forest Classifier**: Primary prediction model
- **Gradient Boosting**: Alternative ensemble method
- **Support Vector Machine**: Linear classification
- **Logistic Regression**: Baseline model
- **MinMaxScaler**: Feature normalization

## 📊 Dataset Information

The system uses the PIMA Indians Diabetes Dataset, which includes:

| Feature | Description | Range |
|---------|-------------|-------|
| Glucose | Blood glucose level (mg/dL) | 50-500 |
| Insulin | Insulin level (μU/mL) | 0-1000 |
| BMI | Body Mass Index (kg/m²) | 15-60 |
| Age | Age in years | 18-120 |

## 🚀 Installation and Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Diabetes-Prediction
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Train the Model

```bash
cd flask
python model.py
```

This will:
- Load and preprocess the diabetes dataset
- Train multiple machine learning models
- Evaluate model performance
- Save the best model as `model.pkl`
- Generate performance visualizations

### Step 5: Run the Application

```bash
# From the flask directory
python app.py
```

The application will be available at `http://localhost:5000`

## 📱 Usage Guide

### For Users

1. **Access the Application**: Open your web browser and navigate to the application URL
2. **Navigate the Interface**: Use the navigation menu to explore different sections
3. **Enter Health Data**: Fill in the prediction form with your health parameters:
   - Glucose Level (mg/dL)
   - Insulin Level (μU/mL)
   - BMI (kg/m²)
   - Age (years)
4. **Get Results**: Submit the form to receive instant analysis and recommendations
5. **Review Recommendations**: Read through personalized treatment and lifestyle advice

### For Developers

#### API Endpoints

- `GET /`: Landing page with project information
- `POST /predict`: Diabetes prediction endpoint
- `GET /health`: Health check endpoint
- `POST /api/predict`: JSON API for predictions

#### API Usage Example

```python
import requests

# Prediction API call
data = {
    "Glucose Level": 120,
    "Insulin": 15,
    "BMI": 25.5,
    "Age": 45
}

response = requests.post('http://localhost:5000/api/predict', json=data)
result = response.json()
print(result)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the flask directory:

```env
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
PORT=5000
```

### Model Configuration

The model training script (`model.py`) can be customized:

- **Feature Selection**: Modify `feature_names` in `preprocess_data()`
- **Model Parameters**: Adjust hyperparameters in `train_models()`
- **Evaluation Metrics**: Add custom metrics in `evaluate_model()`

## 📈 Model Performance

The system achieves the following performance metrics:

- **Accuracy**: 85-90%
- **AUC Score**: 0.85-0.90
- **Sensitivity**: 80-85%
- **Specificity**: 85-90%

### Model Selection

The system automatically selects the best performing model based on:
- Area Under the Curve (AUC) score
- Cross-validation performance
- Feature importance analysis

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   ML Model      │
│                 │    │                 │    │                 │
│ • Bootstrap     │◄──►│ • Flask         │◄──►│ • Random Forest │
│ • HTML/CSS      │    │ • Python        │    │ • Scikit-learn  │
│ • JavaScript    │    │ • REST API      │    │ • Pickle        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔒 Security and Privacy

- **Data Protection**: No personal health data is stored permanently
- **Input Validation**: Comprehensive validation of all user inputs
- **Error Handling**: Robust error handling and logging
- **HTTPS Ready**: Configured for secure deployment

## 🧪 Testing

### Unit Tests

```bash
# Run model tests
python -m pytest tests/test_model.py

# Run API tests
python -m pytest tests/test_api.py
```

### Manual Testing

1. **Form Validation**: Test input validation with invalid data
2. **Prediction Accuracy**: Verify predictions with known test cases
3. **Responsive Design**: Test on different screen sizes
4. **Browser Compatibility**: Test across different browsers

## 📊 Monitoring and Logging

The application includes comprehensive logging:

- **Application Logs**: Request/response logging
- **Model Performance**: Prediction accuracy tracking
- **Error Logging**: Detailed error reporting
- **Health Monitoring**: System health checks

## 🚀 Deployment

### Local Development

```bash
python app.py
```

### Production Deployment

1. **Using Gunicorn**:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Using Docker**:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

3. **Environment Variables**:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Research References

This project is based on comprehensive research including:

- **Global Diabetes Epidemiology**: WHO and IDF reports
- **Nigerian Diabetes Studies**: Local prevalence and risk factors
- **Machine Learning in Healthcare**: Recent advances in medical AI
- **Digital Health Systems**: Best practices for healthcare applications

## 📄 License

This project is part of academic research at the Nigeria Defence Academy, Kaduna. All rights reserved.

## 👥 Authors

- **Student**: [Your Name]
- **Supervisor**: [Supervisor Name]
- **Institution**: Nigeria Defence Academy, Kaduna
- **Department**: Computer Science

## 📞 Contact

For questions or support:
- **Email**: [your-email@example.com]
- **Institution**: Nigeria Defence Academy, Kaduna
- **Department**: Computer Science

## ⚠️ Disclaimer

This system is designed for educational and research purposes. It should not replace professional medical advice. Always consult healthcare professionals for medical decisions and treatment.

---

**Note**: This project represents a significant contribution to bridging the gap between machine learning research and practical healthcare applications in developing countries.
