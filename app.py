# import numpy as np
# import pandas as pd
from flask import Flask, request, jsonify, render_template, flash, send_file
from flask_cors import CORS
import pickle
import os
from datetime import datetime
import logging
from dotenv import load_dotenv
import io
import csv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
CORS(app)

# Load the trained model, scaler, and encoders
model = None
scaler = None
label_encoders = None
feature_names = None

try:
    import os
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, 'models')
    
    # Debug: Log the current directory and models directory
    logger.info(f"Current directory: {current_dir}")
    logger.info(f"Models directory: {models_dir}")
    
    # List all files in the current directory
    logger.info(f"Files in current directory: {os.listdir(current_dir)}")
    
    # Check if models directory exists
    if os.path.exists(models_dir):
        logger.info(f"Models directory exists: {models_dir}")
        logger.info(f"Files in models directory: {os.listdir(models_dir)}")
    else:
        logger.error(f"Models directory does not exist: {models_dir}")
    
    # Load model files with better error handling
    model_path = os.path.join(models_dir, 'model.pkl')
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    encoders_path = os.path.join(models_dir, 'label_encoders.pkl')
    features_path = os.path.join(models_dir, 'feature_names.pkl')
    
    # Check if files exist
    if os.path.exists(model_path):
        logger.info(f"Model file found at: {model_path}")
        model = pickle.load(open(model_path, 'rb'))
        logger.info("Model loaded successfully")
    else:
        logger.error(f"Model file not found at: {model_path}")
    
    if os.path.exists(scaler_path):
        logger.info(f"Scaler file found at: {scaler_path}")
        scaler = pickle.load(open(scaler_path, 'rb'))
        logger.info("Scaler loaded successfully")
    else:
        logger.error(f"Scaler file not found at: {scaler_path}")
    
    if os.path.exists(encoders_path):
        logger.info(f"Label encoders file found at: {encoders_path}")
        label_encoders = pickle.load(open(encoders_path, 'rb'))
        logger.info("Label encoders loaded successfully")
    else:
        logger.error(f"Label encoders file not found at: {encoders_path}")
    
    if os.path.exists(features_path):
        logger.info(f"Feature names file found at: {features_path}")
        feature_names = pickle.load(open(features_path, 'rb'))
        logger.info("Feature names loaded successfully")
    else:
        logger.error(f"Feature names file not found at: {features_path}")
    
    # Check if all components are loaded
    if model is not None and scaler is not None and label_encoders is not None:
        logger.info("All model components loaded successfully")
    else:
        logger.error("Some model components failed to load")
        
except Exception as e:
    logger.error(f"Error loading model: {e}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    model = None
    scaler = None
    label_encoders = None
    feature_names = None

def validate_input_data(data):
    """Validate input data for diabetes prediction"""
    try:
        age = float(data.get('Age', 0))
        gender = data.get('Gender', '')
        bmi = float(data.get('BMI', 0))
        hba1c = float(data.get('HbA1c', 0))
        hypertension = int(data.get('Hypertension', 0))
        heart_disease = int(data.get('HeartDisease', 0))
        smoking_history = data.get('SmokingHistory', '')
        physical_activity = data.get('PhysicalActivity', '')
        dietary_habits = data.get('DietaryHabits', '')
        family_history = data.get('FamilyHistory', '')
        existing_conditions = data.get('ExistingConditions', '')
        
        # Validate ranges based on medical standards
        if not (18 <= age <= 120):
            return False, "Age should be between 18-120 years"
        if gender not in ['Male', 'Female']:
            return False, "Gender should be Male or Female"
        if not (15 <= bmi <= 60):
            return False, "BMI should be between 15-60 kg/m²"
        if not (3.5 <= hba1c <= 9.0):
            return False, "HbA1c should be between 3.5-9.0%"
        if hypertension not in [0, 1]:
            return False, "Hypertension should be 0 (No) or 1 (Yes)"
        if heart_disease not in [0, 1]:
            return False, "Heart Disease should be 0 (No) or 1 (Yes)"
        if smoking_history not in ['never', 'current', 'former', 'No Info']:
            return False, "Invalid smoking history value"
            
        return True, [age, gender, bmi, hba1c, hypertension, heart_disease, smoking_history, 
                     physical_activity, dietary_habits, family_history, existing_conditions]
    except ValueError:
        return False, "Invalid input data. Please enter numeric values where required."

def get_risk_level(prediction_probability):
    """Determine risk level based on prediction probability"""
    if prediction_probability >= 0.8:
        return "High Risk", "danger", "Immediate medical attention required"
    elif prediction_probability >= 0.6:
        return "Moderate Risk", "warning", "Regular monitoring recommended"
    elif prediction_probability >= 0.4:
        return "Low Risk", "info", "Lifestyle modifications advised"
    else:
        return "Very Low Risk", "success", "Continue healthy lifestyle"

def get_diabetes_type(prediction_probability, age, bmi, hba1c):
    """Classify diabetes type based on parameters"""
    if prediction_probability < 0.5:
        return "No Diabetes"
    
    # Simple classification logic based on typical characteristics
    if age < 30 and hba1c > 6.5:
        return "Type 1 Diabetes"
    elif age > 45 and bmi > 25 and hba1c > 6.5:
        return "Type 2 Diabetes"
    elif age > 45 and bmi > 25:
        return "Type 2 Diabetes"
    else:
        return "Type 1 Diabetes"

def get_treatment_recommendations(prediction, risk_level, diabetes_type, input_data):
    """Generate personalized treatment recommendations"""
    recommendations = {
        "immediate": [],
        "lifestyle": [],
        "monitoring": [],
        "medical": [],
        "dietary": [],
        "exercise": []
    }
    
    if prediction == 1:  # Diabetes detected
        recommendations["immediate"].extend([
            "Schedule an appointment with your healthcare provider immediately",
            "Begin monitoring blood glucose levels regularly",
            "Review current medications with your doctor"
        ])
        
        recommendations["lifestyle"].extend([
            "Adopt a low-carbohydrate, high-fiber diet",
            "Engage in at least 150 minutes of moderate exercise weekly",
            "Maintain a healthy weight through balanced nutrition",
            "Limit alcohol consumption and quit smoking",
            "Practice stress management techniques"
        ])
        
        recommendations["monitoring"].extend([
            "Monitor blood glucose levels 2-4 times daily",
            "Track HbA1c levels every 3-6 months",
            "Regular foot examinations",
            "Annual eye examinations",
            "Regular blood pressure monitoring"
        ])
        
        recommendations["medical"].extend([
            "Consider medication therapy (Metformin, Insulin, etc.)",
            "Regular HbA1c testing",
            "Cardiovascular risk assessment",
            "Kidney function monitoring"
        ])
        
        # Dietary recommendations based on diabetes type
        if "Type 2" in diabetes_type:
            recommendations["dietary"].extend([
                "Low-carbohydrate diet (45-50% of calories)",
                "High fiber foods (25-30g daily)",
                "Lean proteins and healthy fats",
                "Limit processed foods and added sugars",
                "Regular meal timing"
            ])
        else:
            recommendations["dietary"].extend([
                "Balanced carbohydrate counting",
                "Regular insulin timing with meals",
                "Consistent meal patterns",
                "Emergency glucose management",
                "Professional nutrition counseling"
            ])
        
        # Exercise recommendations
        recommendations["exercise"].extend([
            "Aerobic exercise: 150 minutes/week moderate intensity",
            "Strength training: 2-3 sessions/week",
            "Flexibility exercises: 2-3 sessions/week",
            "Monitor blood glucose before/after exercise",
            "Stay hydrated during physical activity"
        ])
        
    else:  # No diabetes detected
        recommendations["lifestyle"].extend([
            "Maintain a healthy lifestyle with regular exercise",
            "Eat a balanced diet rich in whole grains and vegetables",
            "Monitor your weight and BMI regularly",
            "Get regular health check-ups",
            "Avoid smoking and limit alcohol consumption"
        ])
        
        recommendations["monitoring"].extend([
            "Annual diabetes screening if over 45 years",
            "Regular BMI monitoring",
            "Blood pressure checks",
            "Cholesterol level monitoring"
        ])
        
        recommendations["dietary"].extend([
            "Balanced diet with whole grains",
            "Plenty of fruits and vegetables",
            "Lean proteins and healthy fats",
            "Limit processed foods",
            "Stay hydrated"
        ])
        
        recommendations["exercise"].extend([
            "150 minutes moderate exercise weekly",
            "Strength training 2-3 times weekly",
            "Flexibility exercises",
            "Find activities you enjoy",
            "Gradual progression in intensity"
        ])
    
    return recommendations

def get_educational_content(diabetes_type, risk_level):
    """Generate educational content based on diabetes type and risk level"""
    content = {
        "general": [
            "Diabetes is a chronic condition affecting how your body processes glucose",
            "Early detection and management can prevent complications",
            "Lifestyle changes are crucial for diabetes management",
            "Regular monitoring helps track progress and prevent complications"
        ],
        "prevention": [
            "Maintain a healthy weight through diet and exercise",
            "Eat a balanced diet low in processed foods",
            "Get regular physical activity",
            "Monitor blood pressure and cholesterol levels",
            "Avoid smoking and limit alcohol consumption"
        ],
        "management": [
            "Work closely with healthcare providers",
            "Monitor blood glucose levels regularly",
            "Take medications as prescribed",
            "Maintain a healthy lifestyle",
            "Attend regular check-ups"
        ]
    }
    
    if "Type 1" in diabetes_type:
        content["specific"] = [
            "Type 1 diabetes is an autoimmune condition",
            "Insulin therapy is essential for survival",
            "Regular blood glucose monitoring is crucial",
            "Carbohydrate counting helps with insulin dosing",
            "Emergency preparedness is important"
        ]
    elif "Type 2" in diabetes_type:
        content["specific"] = [
            "Type 2 diabetes is often related to lifestyle factors",
            "Diet and exercise can help manage blood glucose",
            "Oral medications may be prescribed",
            "Weight management is important",
            "Regular screening for complications is essential"
        ]
    
    return content

@app.route('/')
def home():
    """Landing page with project information"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle diabetes prediction requests"""
    try:
        # Get form data with proper handling of empty values
        def safe_float(value, default=0.0):
            if value == '' or value is None:
                return default
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        
        def safe_int(value, default=0):
            if value == '' or value is None:
                return default
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
        
        age = safe_float(request.form.get('Age', 0))
        gender = request.form.get('Gender', '')
        weight = safe_float(request.form.get('Weight', 0))
        height = safe_float(request.form.get('Height', 0))
        bmi = safe_float(request.form.get('BMI', 0))
        hba1c = safe_float(request.form.get('HbA1c', 0))
        blood_glucose = safe_float(request.form.get('BloodGlucose', 0))
        hypertension = safe_int(request.form.get('Hypertension', 0))
        heart_disease = safe_int(request.form.get('HeartDisease', 0))
        smoking_history = request.form.get('SmokingHistory', '')
        physical_activity = request.form.get('PhysicalActivity', '')
        dietary_habits = request.form.get('DietaryHabits', '')
        family_history = request.form.get('FamilyHistory', '')
        existing_conditions = request.form.get('ExistingConditions', '')
        
        # Validate required fields
        if age <= 0 or bmi <= 0 or hba1c <= 0:
            flash("Please fill in all required fields (Age, BMI, HbA1c)", "error")
            return render_template('index.html', error="Please fill in all required fields")
        
        if not gender:
            flash("Please select your gender", "error")
            return render_template('index.html', error="Please select your gender")
        
        # Check if label_encoders are available
        if label_encoders is None:
            flash("Error: Model encoders not available", "error")
            return render_template('index.html', error="Model encoders not available. Please try again later.")
        
        # Encode categorical variables
        gender_encoded = label_encoders['gender'].transform([gender])[0] if gender in label_encoders['gender'].classes_ else 0
        smoking_encoded = label_encoders['smoking_history'].transform([smoking_history])[0] if smoking_history in label_encoders['smoking_history'].classes_ else 0
        
        # Prepare features for prediction
        features = np.array([age, gender_encoded, bmi, hba1c, hypertension, heart_disease, smoking_encoded]).reshape(1, -1)
        
        # Scale the features
        if scaler is not None:
            features_scaled = scaler.transform(features)
        else:
            flash("Error: Model scaler not available", "error")
            return render_template('index.html', error="Model scaler not available")
        
        # Make prediction
        if model is not None:
            prediction = model.predict(features_scaled)[0]
            prediction_probability = model.predict_proba(features_scaled)[0][1] if hasattr(model, 'predict_proba') else 0.5
            
            # Determine risk level and diabetes type
            risk_level, risk_color, risk_description = get_risk_level(prediction_probability)
            diabetes_type = get_diabetes_type(prediction_probability, age, bmi, hba1c)
            
            # Generate result message
            if prediction == 1:
                prediction_text = f"Diabetes detected. Type: {diabetes_type}. Risk Level: {risk_level}. {risk_description}"
                result_type = "danger"
            else:
                prediction_text = f"No diabetes detected. Risk Level: {risk_level}. {risk_description}"
                result_type = "success"
            
            # Get treatment recommendations and educational content
            input_data = {
                'Age': age, 'Gender': gender, 'Weight': weight, 'Height': height,
                'BMI': bmi, 'HbA1c': hba1c, 'BloodGlucose': blood_glucose,
                'Hypertension': hypertension, 'HeartDisease': heart_disease,
                'SmokingHistory': smoking_history, 'PhysicalActivity': physical_activity,
                'DietaryHabits': dietary_habits, 'FamilyHistory': family_history,
                'ExistingConditions': existing_conditions
            }
            
            recommendations = get_treatment_recommendations(prediction, risk_level, diabetes_type, input_data)
            educational_content = get_educational_content(diabetes_type, risk_level)
            
            # Log the prediction
            logger.info(f"Prediction made - Features: {features[0]}, Prediction: {prediction}, Probability: {prediction_probability:.3f}")
            
            return render_template('index.html', 
                                prediction_text=prediction_text,
                                result_type=result_type,
                                risk_level=risk_level,
                                risk_color=risk_color,
                                prediction_probability=f"{prediction_probability:.1%}",
                                diabetes_type=diabetes_type,
                                recommendations=recommendations,
                                educational_content=educational_content,
                                input_data=input_data)
        else:
            flash("Error: Model not available", "error")
            return render_template('index.html', error="Model not available")
            
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        flash(f"An error occurred during prediction: {str(e)}", "error")
        return render_template('index.html', error=f"An error occurred: {str(e)}")

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for diabetes prediction"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Get data
        age = float(data.get('Age', 0))
        gender = data.get('Gender', '')
        weight = float(data.get('Weight', 0))
        height = float(data.get('Height', 0))
        bmi = float(data.get('BMI', 0))
        hba1c = float(data.get('HbA1c', 0))
        blood_glucose = float(data.get('BloodGlucose', 0))
        hypertension = int(data.get('Hypertension', 0))
        heart_disease = int(data.get('HeartDisease', 0))
        smoking_history = data.get('SmokingHistory', '')
        
        # Check if label_encoders are available
        if label_encoders is None:
            return jsonify({"error": "Model encoders not available"}), 500
        
        # Encode categorical variables
        gender_encoded = label_encoders['gender'].transform([gender])[0] if gender in label_encoders['gender'].classes_ else 0
        smoking_encoded = label_encoders['smoking_history'].transform([smoking_history])[0] if smoking_history in label_encoders['smoking_history'].classes_ else 0
        
        # Prepare features for prediction
        features = np.array([age, gender_encoded, bmi, hba1c, hypertension, heart_disease, smoking_encoded]).reshape(1, -1)
        
        # Scale the features
        if scaler is not None:
            features_scaled = scaler.transform(features)
        else:
            return jsonify({"error": "Model scaler not available"}), 500
        
        # Make prediction
        if model is not None:
            prediction = model.predict(features_scaled)[0]
            prediction_probability = model.predict_proba(features_scaled)[0][1] if hasattr(model, 'predict_proba') else 0.5
            
            # Determine risk level and diabetes type
            risk_level, risk_color, risk_description = get_risk_level(prediction_probability)
            diabetes_type = get_diabetes_type(prediction_probability, age, bmi, hba1c)
            
            # Get treatment recommendations
            input_data = {
                'Age': age, 'Gender': gender, 'Weight': weight, 'Height': height,
                'BMI': bmi, 'HbA1c': hba1c, 'BloodGlucose': blood_glucose,
                'Hypertension': hypertension, 'HeartDisease': heart_disease,
                'SmokingHistory': smoking_history
            }
            
            recommendations = get_treatment_recommendations(prediction, risk_level, diabetes_type, input_data)
            
            response = {
                "prediction": int(prediction),
                "prediction_probability": float(prediction_probability),
                "risk_level": risk_level,
                "risk_color": risk_color,
                "risk_description": risk_description,
                "diabetes_type": diabetes_type,
                "recommendations": recommendations,
                "timestamp": datetime.now().isoformat()
            }
            
            return jsonify(response)
        else:
            return jsonify({"error": "Model not available"}), 500
            
    except Exception as e:
        logger.error(f"API Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/export-report', methods=['POST'])
def export_report():
    """Export prediction report as CSV"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Diabetes Prediction Report'])
        writer.writerow(['Generated on', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])
        
        # Write patient information
        writer.writerow(['Patient Information'])
        writer.writerow(['Age', data.get('Age', 'N/A')])
        writer.writerow(['Gender', data.get('Gender', 'N/A')])
        writer.writerow(['Weight (kg)', data.get('Weight', 'N/A')])
        writer.writerow(['Height (cm)', data.get('Height', 'N/A')])
        writer.writerow(['BMI', data.get('BMI', 'N/A')])
        writer.writerow(['HbA1c (%)', data.get('HbA1c', 'N/A')])
        writer.writerow(['Blood Glucose (mg/dL)', data.get('BloodGlucose', 'N/A')])
        writer.writerow(['Hypertension', 'Yes' if data.get('Hypertension', 0) else 'No'])
        writer.writerow(['Heart Disease', 'Yes' if data.get('HeartDisease', 0) else 'No'])
        writer.writerow(['Smoking History', data.get('SmokingHistory', 'N/A')])
        writer.writerow(['Physical Activity', data.get('PhysicalActivity', 'N/A')])
        writer.writerow(['Dietary Habits', data.get('DietaryHabits', 'N/A')])
        writer.writerow(['Family History', data.get('FamilyHistory', 'N/A')])
        writer.writerow(['Existing Conditions', data.get('ExistingConditions', 'N/A')])
        writer.writerow([])
        
        # Write prediction results
        writer.writerow(['Prediction Results'])
        writer.writerow(['Prediction', 'Diabetes' if data.get('prediction', 0) else 'No Diabetes'])
        writer.writerow(['Probability', f"{data.get('prediction_probability', 0):.1%}"])
        writer.writerow(['Risk Level', data.get('risk_level', 'N/A')])
        writer.writerow(['Diabetes Type', data.get('diabetes_type', 'N/A')])
        writer.writerow([])
        
        # Write recommendations
        recommendations = data.get('recommendations', {})
        writer.writerow(['Recommendations'])
        for category, items in recommendations.items():
            if items:
                writer.writerow([category.title()])
                for item in items:
                    writer.writerow(['', item])
                writer.writerow([])
        
        # Prepare response
        output.seek(0)
        csv_content = output.getvalue()
        
        return send_file(
            io.BytesIO(csv_content.encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'diabetes_prediction_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        logger.error(f"Export Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "encoders_loaded": label_encoders is not None,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/debug')
def debug():
    """Debug endpoint to check file availability"""
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, 'models')
    
    debug_info = {
        "current_directory": current_dir,
        "models_directory": models_dir,
        "models_directory_exists": os.path.exists(models_dir),
        "files_in_current_dir": os.listdir(current_dir) if os.path.exists(current_dir) else [],
        "files_in_models_dir": os.listdir(models_dir) if os.path.exists(models_dir) else [],
        "model_file_exists": os.path.exists(os.path.join(models_dir, 'model.pkl')),
        "scaler_file_exists": os.path.exists(os.path.join(models_dir, 'scaler.pkl')),
        "encoders_file_exists": os.path.exists(os.path.join(models_dir, 'label_encoders.pkl')),
        "features_file_exists": os.path.exists(os.path.join(models_dir, 'feature_names.pkl')),
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "encoders_loaded": label_encoders is not None,
        "features_loaded": feature_names is not None
    }
    
    return jsonify(debug_info)

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', error="Internal server error"), 500

# WSGI application for Vercel
app.debug = False

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5050))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting DiabetesCare AI application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
