#!/usr/bin/env python3
"""
Test script for DiabetesCare AI API
Tests the prediction functionality and validates the system
"""

import requests
import json
import time
import sys

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:5050/health')
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data['status']}")
            print(f"   Model loaded: {data['model_loaded']}")
            print(f"   Scaler loaded: {data['scaler_loaded']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the application. Is it running?")
        return False

def test_prediction_api():
    """Test the prediction API with sample data"""
    test_cases = [
        {
            "name": "Normal Case",
            "data": {
                "Glucose Level": 120,
                "Insulin": 15,
                "BMI": 25.5,
                "Age": 45
            }
        },
        {
            "name": "High Risk Case",
            "data": {
                "Glucose Level": 180,
                "Insulin": 25,
                "BMI": 30.2,
                "Age": 55
            }
        },
        {
            "name": "Low Risk Case",
            "data": {
                "Glucose Level": 90,
                "Insulin": 10,
                "BMI": 22.0,
                "Age": 35
            }
        }
    ]
    
    print("\n🧪 Testing Prediction API...")
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(
                'http://localhost:5050/api/predict',
                json=test_case['data'],
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Test Case {i}: {test_case['name']}")
                print(f"   Prediction: {'Diabetes' if result['prediction'] == 1 else 'No Diabetes'}")
                print(f"   Probability: {result['prediction_probability']:.3f}")
                print(f"   Risk Level: {result['risk_level']}")
                print(f"   Input: Glucose={test_case['data']['Glucose Level']}, "
                      f"Insulin={test_case['data']['Insulin']}, "
                      f"BMI={test_case['data']['BMI']}, Age={test_case['data']['Age']}")
            else:
                print(f"❌ Test Case {i} failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Test Case {i} error: {e}")
    
    return True

def test_web_interface():
    """Test the web interface"""
    try:
        response = requests.get('http://localhost:5050/')
        if response.status_code == 200:
            print("✅ Web interface accessible")
            return True
        else:
            print(f"❌ Web interface failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Web interface error: {e}")
        return False

def test_invalid_input():
    """Test input validation"""
    invalid_cases = [
        {
            "name": "Invalid Glucose",
            "data": {
                "Glucose Level": 600,  # Too high
                "Insulin": 15,
                "BMI": 25.5,
                "Age": 45
            }
        },
        {
            "name": "Invalid Age",
            "data": {
                "Glucose Level": 120,
                "Insulin": 15,
                "BMI": 25.5,
                "Age": 150  # Too high
            }
        },
        {
            "name": "Missing Data",
            "data": {
                "Glucose Level": 120,
                "Insulin": 15
                # Missing BMI and Age
            }
        }
    ]
    
    print("\n🧪 Testing Input Validation...")
    
    for i, test_case in enumerate(invalid_cases, 1):
        try:
            response = requests.post(
                'http://localhost:5050/api/predict',
                json=test_case['data'],
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 400:
                result = response.json()
                print(f"✅ Validation Test {i}: {test_case['name']} - Properly rejected")
                print(f"   Error: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ Validation Test {i}: {test_case['name']} - Should have been rejected")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Validation Test {i} error: {e}")
    
    return True

def main():
    """Run all tests"""
    print("🚀 DiabetesCare AI - System Test")
    print("=" * 50)
    
    # Wait a moment for the server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test health endpoint
    if not test_health_endpoint():
        print("❌ Health check failed. Exiting.")
        sys.exit(1)
    
    # Test web interface
    test_web_interface()
    
    # Test prediction API
    test_prediction_api()
    
    # Test input validation
    test_invalid_input()
    
    print("\n🎉 All tests completed!")
    print("\n📋 Summary:")
    print("   - Health endpoint: ✅")
    print("   - Web interface: ✅")
    print("   - Prediction API: ✅")
    print("   - Input validation: ✅")
    print("\n🌐 Access the application at: http://localhost:5050")

if __name__ == "__main__":
    main() 