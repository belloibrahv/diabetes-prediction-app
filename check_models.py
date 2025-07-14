#!/usr/bin/env python3
"""
Script to check if model files are present and can be loaded
This helps diagnose deployment issues on Render
"""

import os
import pickle
import sys

def check_models():
    """Check if all model files exist and can be loaded"""
    print("🔍 Checking model files...")
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, 'models')
    
    print(f"📁 Current directory: {current_dir}")
    print(f"📁 Models directory: {models_dir}")
    
    # Check if models directory exists
    if not os.path.exists(models_dir):
        print("❌ Models directory does not exist!")
        return False
    
    print("✅ Models directory exists")
    
    # List files in models directory
    try:
        files = os.listdir(models_dir)
        print(f"📋 Files in models directory: {files}")
    except Exception as e:
        print(f"❌ Error listing files: {e}")
        return False
    
    # Check each model file
    required_files = ['model.pkl', 'scaler.pkl', 'label_encoders.pkl', 'feature_names.pkl']
    all_good = True
    
    for filename in required_files:
        file_path = os.path.join(models_dir, filename)
        
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ {filename} exists ({file_size} bytes)")
            
            # Try to load the file
            try:
                with open(file_path, 'rb') as f:
                    data = pickle.load(f)
                print(f"✅ {filename} loaded successfully")
            except Exception as e:
                print(f"❌ {filename} failed to load: {e}")
                all_good = False
        else:
            print(f"❌ {filename} not found")
            all_good = False
    
    if all_good:
        print("\n🎉 All model files are present and loadable!")
        return True
    else:
        print("\n❌ Some model files are missing or corrupted!")
        return False

if __name__ == "__main__":
    success = check_models()
    sys.exit(0 if success else 1) 