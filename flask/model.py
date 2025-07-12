#!/usr/bin/env python
# coding: utf-8

"""
Diabetes Prediction Model Training Script
Online Diabetes Check and Treatment Recommendation System with Machine Learning

This script implements the machine learning model development process as described in the research paper.
It includes data preprocessing, feature engineering, model selection, and evaluation.
Updated to use new dataset and remove insulin/glucose parameters as per supervisor feedback.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.feature_selection import SelectKBest, f_classif
import warnings
import pickle
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

warnings.filterwarnings('ignore')

class DiabetesPredictionModel:
    """Diabetes prediction model with comprehensive training and evaluation"""
    
    def __init__(self):
        self.dataset = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = None
        self.model = None
        self.feature_names = None
        self.label_encoders = {}
        
    def load_data(self, file_path='../diabetes_prediction_dataset.csv'):
        """Load and explore the diabetes dataset"""
        try:
            self.dataset = pd.read_csv(file_path)
            logger.info(f"Dataset loaded successfully with {self.dataset.shape[0]} samples and {self.dataset.shape[1]} features")
            
            # Display dataset information
            print("Dataset Info:")
            print(f"Shape: {self.dataset.shape}")
            print(f"Features: {list(self.dataset.columns)}")
            print(f"Target distribution:\n{self.dataset['diabetes'].value_counts()}")
            
            return True
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return False
    
    def explore_data(self):
        """Perform exploratory data analysis"""
        print("\n=== EXPLORATORY DATA ANALYSIS ===")
        
        # Basic statistics
        print("\nBasic Statistics:")
        print(self.dataset.describe())
        
        # Check for missing values
        print("\nMissing Values:")
        print(self.dataset.isnull().sum())
        
        # Correlation analysis (only numerical features)
        numerical_features = ['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'diabetes']
        correlation_matrix = self.dataset[numerical_features].corr()
        plt.figure(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Feature Correlation Matrix')
        plt.tight_layout()
        plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Distribution plots for numerical features
        numerical_features = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        for i, feature in enumerate(numerical_features):
            row = i // 2
            col = i % 2
            axes[row, col].hist(self.dataset[feature], bins=30, alpha=0.7, edgecolor='black')
            axes[row, col].set_title(f'{feature.replace("_", " ").title()} Distribution')
            axes[row, col].set_xlabel(feature.replace("_", " ").title())
            axes[row, col].set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('feature_distributions.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Outcome distribution
        plt.figure(figsize=(8, 6))
        outcome_counts = self.dataset['diabetes'].value_counts()
        plt.pie(outcome_counts.values, labels=['No Diabetes', 'Diabetes'], autopct='%1.1f%%')
        plt.title('Diabetes Outcome Distribution')
        plt.savefig('outcome_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Categorical feature analysis
        categorical_features = ['gender', 'hypertension', 'heart_disease', 'smoking_history']
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        for i, feature in enumerate(categorical_features):
            row = i // 2
            col = i % 2
            value_counts = self.dataset[feature].value_counts()
            axes[row, col].bar(value_counts.index, value_counts.values)
            axes[row, col].set_title(f'{feature.replace("_", " ").title()} Distribution')
            axes[row, col].set_xlabel(feature.replace("_", " ").title())
            axes[row, col].set_ylabel('Count')
            axes[row, col].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('categorical_distributions.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def preprocess_data(self):
        """Preprocess the data for machine learning"""
        print("\n=== DATA PREPROCESSING ===")
        
        # Create a copy for preprocessing
        df = self.dataset.copy()
        
        # Handle categorical variables
        categorical_features = ['gender', 'smoking_history']
        for feature in categorical_features:
            le = LabelEncoder()
            df[feature] = le.fit_transform(df[feature])
            self.label_encoders[feature] = le
        
        # Select features based on research requirements (removing insulin and glucose)
        # Using comprehensive features: Age, Gender, BMI, HbA1c, PhysicalActivity, DietaryHabits, FamilyHistory, ExistingConditions
        self.feature_names = [
            'age', 'gender', 'bmi', 'HbA1c_level', 
            'hypertension', 'heart_disease', 'smoking_history'
        ]
        
        X = df[self.feature_names].values
        y = df['diabetes'].values
        
        print(f"Selected features: {self.feature_names}")
        print(f"Feature matrix shape: {X.shape}")
        print(f"Target vector shape: {y.shape}")
        
        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training set size: {self.X_train.shape[0]}")
        print(f"Test set size: {self.X_test.shape[0]}")
        
        # Scale the features
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print("Data preprocessing completed successfully")
    
    def train_models(self):
        """Train multiple models and select the best one"""
        print("\n=== MODEL TRAINING ===")
        
        models = {
            'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
            'Gradient Boosting': GradientBoostingClassifier(random_state=42),
            'SVM': SVC(random_state=42, probability=True),
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
        }
        
        results = {}
        
        for name, model in models.items():
            print(f"\nTraining {name}...")
            
            # Train the model
            model.fit(self.X_train_scaled, self.y_train)
            
            # Make predictions
            y_pred = model.predict(self.X_test_scaled)
            y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
            
            # Calculate metrics
            accuracy = model.score(self.X_test_scaled, self.y_test)
            auc_score = roc_auc_score(self.y_test, y_pred_proba)
            
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'auc_score': auc_score,
                'predictions': y_pred,
                'probabilities': y_pred_proba
            }
            
            print(f"{name} - Accuracy: {accuracy:.4f}, AUC: {auc_score:.4f}")
        
        # Select the best model based on AUC score
        best_model_name = max(results.keys(), key=lambda x: results[x]['auc_score'])
        self.model = results[best_model_name]['model']
        
        print(f"\nBest model: {best_model_name}")
        print(f"Best AUC score: {results[best_model_name]['auc_score']:.4f}")
        
        return results
    
    def evaluate_model(self, results):
        """Comprehensive model evaluation"""
        print("\n=== MODEL EVALUATION ===")
        
        # Get the best model results
        best_model_name = max(results.keys(), key=lambda x: results[x]['auc_score'])
        best_results = results[best_model_name]
        
        # Classification report
        print(f"\nClassification Report for {best_model_name}:")
        print(classification_report(self.y_test, best_results['predictions']))
        
        # Confusion matrix
        cm = confusion_matrix(self.y_test, best_results['predictions'])
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {best_model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # ROC curve
        plt.figure(figsize=(8, 6))
        fpr, tpr, _ = roc_curve(self.y_test, best_results['probabilities'])
        plt.plot(fpr, tpr, label=f'{best_model_name} (AUC = {best_results["auc_score"]:.3f})')
        plt.plot([0, 1], [0, 1], 'k--', label='Random')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend()
        plt.grid(True)
        plt.savefig('roc_curve.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Feature importance (for tree-based models)
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = self.model.feature_importances_
            plt.figure(figsize=(10, 6))
            plt.bar(self.feature_names, feature_importance)
            plt.title('Feature Importance')
            plt.xlabel('Features')
            plt.ylabel('Importance')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"\nFeature Importance:")
            for feature, importance in zip(self.feature_names, feature_importance):
                print(f"{feature}: {importance:.4f}")
    
    def save_model(self):
        """Save the trained model and scaler"""
        print("\n=== SAVING MODEL ===")
        
        try:
            # Save the model
            with open('model.pkl', 'wb') as f:
                pickle.dump(self.model, f)
            
            # Save the scaler
            with open('scaler.pkl', 'wb') as f:
                pickle.dump(self.scaler, f)
            
            # Save the label encoders
            with open('label_encoders.pkl', 'wb') as f:
                pickle.dump(self.label_encoders, f)
            
            # Save feature names
            with open('feature_names.pkl', 'wb') as f:
                pickle.dump(self.feature_names, f)
            
            print("Model, scaler, and encoders saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False
    
    def test_model(self):
        """Test the model with sample data"""
        print("\n=== MODEL TESTING ===")
        
        # Sample test cases
        test_cases = [
            [45, 0, 25.5, 5.7, 0, 0, 0],  # Normal case (Female, no conditions)
            [65, 1, 30.2, 7.2, 1, 1, 2],  # High risk case (Male, with conditions)
            [35, 0, 22.0, 5.0, 0, 0, 0],  # Low risk case (Female, healthy)
        ]
        
        test_cases_scaled = self.scaler.transform(np.array(test_cases))
        predictions = self.model.predict(test_cases_scaled)
        probabilities = self.model.predict_proba(test_cases_scaled)[:, 1]
        
        print("Sample Predictions:")
        for i, (case, pred, prob) in enumerate(zip(test_cases, predictions, probabilities)):
            status = "Diabetes" if pred == 1 else "No Diabetes"
            print(f"Case {i+1}: Age={case[0]}, Gender={'Male' if case[1] else 'Female'}, BMI={case[2]}, HbA1c={case[3]}")
            print(f"  Prediction: {status}, Probability: {prob:.3f}")

def main():
    """Main function to run the complete model training pipeline"""
    print("=== DIABETES PREDICTION MODEL TRAINING ===")
    print("Online Diabetes Check and Treatment Recommendation System with Machine Learning")
    print("Updated to remove insulin and glucose parameters as per supervisor feedback")
    print("=" * 80)
    
    # Initialize the model
    model_trainer = DiabetesPredictionModel()
    
    # Load data
    if not model_trainer.load_data():
        print("Failed to load dataset. Exiting.")
        return
    
    # Explore data
    model_trainer.explore_data()
    
    # Preprocess data
    model_trainer.preprocess_data()
    
    # Train models
    results = model_trainer.train_models()
    
    # Evaluate models
    model_trainer.evaluate_model(results)
    
    # Save model
    if model_trainer.save_model():
        print("Model training completed successfully!")
        
        # Test the model
        model_trainer.test_model()
    else:
        print("Failed to save model.")

if __name__ == "__main__":
    main()


