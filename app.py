# app.py
import json
import os
from datetime import datetime
import logging
from functools import wraps

from flask import Flask, request, jsonify, render_template, flash, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from dotenv import load_dotenv
import io
import csv
import numpy as np

# Load environment variables from .env file
load_dotenv()

# Configure logging for better error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_super_secret_key_please_change_this_in_production_environment')
CORS(app)

USERS_FILE = 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.warning(f"Error decoding JSON from {USERS_FILE}. Returning empty users dictionary.")
        return {}
    except Exception as e:
        logger.error(f"Error loading users from {USERS_FILE}: {e}")
        return {}

def save_users(users):
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving users to {USERS_FILE}: {e}")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "info")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def rule_based_predict(age, bmi, hba1c):
    diabetes_type = "No Diabetes"
    risk_level = "Low Risk"
    prediction = 0
    explanation = []
    rec_category = "Lifestyle, Dietary"
    
    if hba1c > 6.5 and age < 30:
        diabetes_type = "Type 1 Diabetes"
        risk_level = "High Risk"
        prediction = 1
        rec_category = "Medical, Monitoring"
        explanation.append("Rule R1: Age < 30 and HbA1c > 6.5% suggests Type 1 Diabetes.")
    elif hba1c > 6.5 and age >= 30:
        diabetes_type = "Type 2 Diabetes"
        risk_level = "High Risk"
        prediction = 1
        rec_category = "Medical, Lifestyle, Dietary"
        explanation.append("Rule R2: Age >= 30 and HbA1c > 6.5% suggests Type 2 Diabetes.")
    elif 5.7 <= hba1c <= 6.4:
        diabetes_type = "Prediabetes"
        risk_level = "Moderate Risk"
        prediction = 0
        rec_category = "Lifestyle, Dietary, Medical"
        explanation.append("Rule R3: HbA1c between 5.7% and 6.4% indicates Prediabetes.")
    elif hba1c < 5.7 and 25 <= bmi < 30:
        diabetes_type = "No Diabetes"
        risk_level = "Moderate Risk"
        prediction = 0
        rec_category = "Lifestyle, Dietary"
        explanation.append("Rule R4: BMI 25-29.9 and HbA1c < 5.7% indicates Moderate Risk (Overweight).")
    elif hba1c < 5.7 and bmi >= 30:
        diabetes_type = "No Diabetes"
        risk_level = "Moderate Risk"
        prediction = 0
        rec_category = "Lifestyle, Dietary"
        explanation.append("Rule R5: BMI >= 30 and HbA1c < 5.7% indicates Moderate Risk (Obese).")
    elif hba1c < 5.7 and bmi < 25:
        diabetes_type = "No Diabetes"
        risk_level = "Low Risk"
        prediction = 0
        rec_category = "Lifestyle, Dietary"
        explanation.append("Rule R6: BMI < 25 and HbA1c < 5.7% indicates Low Risk.")
    else:
        explanation.append("Input does not match any specific rule. Defaulting to low risk.")
    return prediction, risk_level, diabetes_type, rec_category, explanation

def get_treatment_recommendations(prediction, risk_level, diabetes_type, input_data):
    recommendations = {
        "immediate": [],
        "lifestyle": [],
        "monitoring": [],
        "medical": [],
        "dietary": [],
        "exercise": []
    }
    if prediction == 1:
        recommendations["immediate"].extend([
            "Schedule an appointment with your healthcare provider immediately to confirm diagnosis and develop a treatment plan.",
            "Begin monitoring blood glucose levels regularly as advised by your doctor.",
            "Review current medications with your doctor to ensure they are appropriate for diabetes management."
        ])
        recommendations["lifestyle"].extend([
            "Adopt a low-carbohydrate, high-fiber diet focusing on whole foods and portion control.",
            "Engage in at least 150 minutes of moderate-intensity aerobic exercise weekly (e.g., brisk walking, cycling).",
            "Maintain a healthy weight through balanced nutrition and regular physical activity.",
            "Limit alcohol consumption and quit smoking entirely, as both can worsen diabetes complications.",
            "Practice stress management techniques like meditation, yoga, or deep breathing exercises."
        ])
        recommendations["monitoring"].extend([
            "Monitor blood glucose levels 2-4 times daily, or as recommended by your healthcare provider.",
            "Track HbA1c levels every 3-6 months to assess long-term blood sugar control.",
            "Perform regular foot examinations to check for cuts, sores, or infections.",
            "Undergo annual eye examinations to screen for diabetic retinopathy.",
            "Monitor blood pressure regularly and manage it within target ranges."
        ])
        recommendations["medical"].extend([
            "Discuss medication therapy options (e.g., Metformin, Insulin, SGLT2 inhibitors) with your doctor.",
            "Ensure regular HbA1c testing is performed as part of your diabetes management plan.",
            "Undergo cardiovascular risk assessment to manage heart health.",
            "Monitor kidney function regularly through blood and urine tests."
        ])
        if "Type 2" in diabetes_type:
            recommendations["dietary"].extend([
                "Focus on a low-carbohydrate diet (e.g., 45-50% of total daily calories from carbs).",
                "Incorporate high fiber foods (25-30g daily) such as whole grains, fruits, and vegetables.",
                "Prioritize lean proteins (chicken, fish, beans) and healthy fats (avocado, nuts, olive oil).",
                "Strictly limit processed foods, sugary drinks, and added sugars.",
                "Maintain regular meal timing to help stabilize blood glucose levels."
            ])
        else:
            recommendations["dietary"].extend([
                "Implement balanced carbohydrate counting to match insulin doses.",
                "Ensure regular insulin timing in conjunction with meals.",
                "Maintain consistent meal patterns to avoid blood sugar fluctuations.",
                "Understand emergency glucose management for hypoglycemia.",
                "Seek professional nutrition counseling for personalized meal planning."
            ])
        recommendations["exercise"].extend([
            "Aim for at least 150 minutes per week of moderate-intensity aerobic exercise.",
            "Include strength training exercises 2-3 sessions per week for all major muscle groups.",
            "Incorporate flexibility exercises (stretching, yoga) 2-3 sessions per week.",
            "Monitor blood glucose before and after exercise, especially if on insulin or certain medications.",
            "Stay well-hydrated during physical activity."
        ])
    else:
        recommendations["lifestyle"].extend([
            "Maintain a healthy lifestyle with regular exercise to prevent diabetes.",
            "Eat a balanced diet rich in whole grains, lean proteins, and plenty of fruits and vegetables.",
            "Monitor your weight and BMI regularly to stay within a healthy range.",
            "Get regular health check-ups, especially if you have risk factors for diabetes.",
            "Avoid smoking and limit alcohol consumption to support overall health."
        ])
        recommendations["monitoring"].extend([
            "Consider annual diabetes screening if you are over 45 years old or have other risk factors.",
            "Regularly monitor your BMI and weight.",
            "Have your blood pressure checked regularly.",
            "Monitor your cholesterol levels as part of routine health checks."
        ])
        recommendations["dietary"].extend([
            "Follow a balanced diet with an emphasis on whole grains over refined grains.",
            "Consume plenty of fruits and vegetables daily.",
            "Include lean proteins and healthy fats in your meals.",
            "Limit processed foods, sugary drinks, and excessive saturated/trans fats.",
            "Stay well-hydrated by drinking adequate water throughout the day."
        ])
        recommendations["exercise"].extend([
            "Aim for at least 150 minutes of moderate-intensity exercise weekly.",
            "Incorporate strength training 2-3 times weekly.",
            "Include flexibility exercises in your routine.",
            "Find physical activities you enjoy to make exercise sustainable.",
            "Progress gradually in intensity and duration to avoid injury."
        ])
    return recommendations

def get_educational_content(diabetes_type, risk_level):
    content = {
        "general": [
            "Diabetes is a chronic condition affecting how your body processes glucose (sugar).",
            "Early detection and proper management can prevent or delay serious complications.",
            "Lifestyle changes, including diet and exercise, are crucial for diabetes management and prevention.",
            "Regular monitoring of blood sugar levels helps track progress and prevent complications."
        ],
        "prevention": [
            "Maintain a healthy weight through a balanced diet and regular exercise.",
            "Eat a balanced diet low in processed foods, sugary drinks, and unhealthy fats.",
            "Get at least 150 minutes of moderate physical activity each week.",
            "Monitor blood pressure and cholesterol levels regularly.",
            "Avoid smoking and limit alcohol consumption."
        ],
        "management": [
            "Work closely with your healthcare providers to develop a personalized care plan.",
            "Monitor blood glucose levels regularly as advised by your doctor.",
            "Take medications as prescribed and understand their purpose.",
            "Maintain a healthy lifestyle, including diet and exercise, as a cornerstone of management.",
            "Attend regular check-ups and screenings for diabetes complications."
        ],
        "specific": []
    }
    if "Type 1" in diabetes_type:
        content["specific"].extend([
            "Type 1 diabetes is an autoimmune condition where the body does not produce insulin.",
            "Insulin therapy is essential for survival and must be administered daily.",
            "Regular blood glucose monitoring is crucial for adjusting insulin doses.",
            "Carbohydrate counting helps match insulin doses to food intake.",
            "Emergency preparedness for hypoglycemia (low blood sugar) is important."
        ])
    elif "Type 2" in diabetes_type:
        content["specific"].extend([
            "Type 2 diabetes is often related to insulin resistance and insufficient insulin production, frequently linked to lifestyle factors.",
            "Diet and exercise are powerful tools to help manage blood glucose levels.",
            "Oral medications or injectable non-insulin medications may be prescribed.",
            "Weight management is a key component in managing Type 2 diabetes.",
            "Regular screening for complications (eyes, kidneys, nerves, heart) is essential."
        ])

    elif "Prediabetes" in diabetes_type:
        content["specific"].extend([
            "Prediabetes means your blood sugar is higher than normal but not yet diabetes.",
            "This is a critical time for intervention; lifestyle changes can prevent Type 2 diabetes.",
            "Focus on increasing physical activity and making healthier food choices.",
            "Losing even a small amount of weight can make a big difference.",
            "Regular check-ups are important to monitor your blood sugar levels."
        ])
    return content

@app.route('/')
@login_required
def home():
    username = session.get('username')
    return render_template('index.html', username=username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        users = load_users()
        if not username or not password or not email:
            flash("All fields are required.", "error")
            return render_template('register.html', username=username, email=email)
        if username in users:
            flash("Username already exists. Please choose a different one.", "warning")
            return render_template('register.html', username=username, email=email)
        hashed_password = generate_password_hash(password)
        user_id = str(len(users) + 1)
        users[username] = {
            'user_id': user_id,
            'password_hash': hashed_password,
            'email': email,
            'created_at': datetime.now().isoformat(),
            'predictions': []
        }
        save_users(users)
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = load_users()
        user_data = users.get(username)
        if user_data and check_password_hash(user_data['password_hash'], password):
            session['user_id'] = user_data['user_id']
            session['username'] = username
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.", "error")
            return render_template('login.html', username=username)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        def safe_float(value, default=0.0):
            if value == '' or value is None:
                return default
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        age = safe_float(request.form.get('Age', 0))
        bmi = safe_float(request.form.get('BMI', 0))
        hba1c = safe_float(request.form.get('HbA1c', 0))
        
        if age <= 0 or bmi <= 0 or hba1c <= 0:
            flash("Please fill in all required fields (Age, BMI, HbA1c) with valid numbers.", "error")
            input_data = {'Age': age, 'BMI': bmi, 'HbA1c': hba1c}
            return render_template('index.html', input_data=input_data, username=session.get('username'))
        
        prediction, risk_level, diabetes_type, rec_category, explanation = rule_based_predict(age, bmi, hba1c)
        
        if prediction == 1:
            prediction_text = f"Diabetes detected. Type: {diabetes_type}. Risk Level: {risk_level}."
            result_type = "danger"
        else:
            prediction_text = f"No diabetes detected. Risk Level: {risk_level}."
            result_type = "success"
        
        input_data = {'Age': age, 'BMI': bmi, 'HbA1c': hba1c}
        recommendations = get_treatment_recommendations(prediction, risk_level, diabetes_type, input_data)
        educational_content = get_educational_content(diabetes_type, risk_level)
        
        return render_template('index.html',
            prediction_text=prediction_text,
            result_type=result_type,
            risk_level=risk_level,
            diabetes_type=diabetes_type,
            recommendations=recommendations,
            educational_content=educational_content,
            input_data=input_data,
            explanation=explanation,
            username=session.get('username')
        )
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        flash(f"An unexpected error occurred during prediction: {str(e)}", "error")
        input_data = {'Age': request.form.get('Age', ''), 'BMI': request.form.get('BMI', ''), 'HbA1c': request.form.get('HbA1c', '')}
        return render_template('index.html', error=f"An error occurred: {str(e)}", input_data=input_data, username=session.get('username'))

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        age = float(data.get('Age', 0))
        bmi = float(data.get('BMI', 0))
        hba1c = float(data.get('HbA1c', 0))
        
        prediction, risk_level, diabetes_type, rec_category, explanation = rule_based_predict(age, bmi, hba1c)
        input_data = {'Age': age, 'BMI': bmi, 'HbA1c': hba1c}
        recommendations = get_treatment_recommendations(prediction, risk_level, diabetes_type, input_data)
        
        response = {
            "prediction": int(prediction),
            "risk_level": risk_level,
            "diabetes_type": diabetes_type,
            "recommendations": recommendations,
            "explanation": explanation,
            "timestamp": datetime.now().isoformat()
        }
        return jsonify(response)
    except Exception as e:
        logger.error(f"API Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/export-report', methods=['POST'])
@login_required
def export_report():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided for export"}), 400
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Diabetes Prediction Report'])
        writer.writerow(['Generated on', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow(['Generated for User', session.get('username', 'Anonymous')])
        writer.writerow([])
        writer.writerow(['Patient Information'])
        writer.writerow(['Age', data.get('Age', 'N/A')])
        writer.writerow(['BMI', data.get('BMI', 'N/A')])
        writer.writerow(['HbA1c (%)', data.get('HbA1c', 'N/A')])
        writer.writerow([])
        writer.writerow(['Prediction Results'])
        writer.writerow(['Prediction', 'Diabetes' if data.get('prediction', 0) else 'No Diabetes'])
        writer.writerow(['Risk Level', data.get('risk_level', 'N/A')])
        writer.writerow(['Diabetes Type', data.get('diabetes_type', 'N/A')])
        writer.writerow([])
        recommendations = data.get('recommendations', {})
        writer.writerow(['Recommendations'])
        for category, items in recommendations.items():
            if items:
                writer.writerow([category.title()])
                for item in items:
                    writer.writerow(['', item])
                writer.writerow([])
        output.seek(0)
        csv_content = output.getvalue()
        from flask import send_file
        return send_file(
            io.BytesIO(csv_content.encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'diabetes_prediction_report_{session.get("username", "anonymous")}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    except Exception as e:
        logger.error(f"Export Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    flash("The page you requested could not be found.", "error")
    return render_template('index.html', error="Page not found", username=session.get('username')), 404

@app.errorhandler(500)
def internal_error(error):
    flash("An internal server error occurred. Please try again later.", "error")
    return render_template('index.html', error="Internal server error", username=session.get('username')), 500

app.debug = False

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5050))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    logger.info(f"Starting DiabetesCare AI application on port {port} with debug={debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)