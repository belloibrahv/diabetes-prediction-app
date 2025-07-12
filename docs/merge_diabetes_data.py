"""
merge_diabetes_data.py

Standalone script to merge and clean multiple diabetes-related CSV datasets into a unified diabetes.csv file.

Instructions:
1. Place all source CSV files in a folder named 'data_sources/' in the project root.
2. Run this script: python merge_diabetes_data.py
3. The merged and cleaned dataset will be saved as 'diabetes.csv' in the project root.

Expected unified columns:
- Age, Gender, BMI, Weight, Height, HbA1c, PhysicalActivity, DietaryHabits, FamilyHistory, ExistingConditions, DiabetesType, Outcome
"""
import os
import glob
import pandas as pd
import numpy as np

# Unified column names (Insulin and Glucose removed)
COLUMNS = [
    'Age', 'Gender', 'BMI', 'Weight', 'Height', 'HbA1c',
    'PhysicalActivity', 'DietaryHabits', 'FamilyHistory', 'ExistingConditions', 'DiabetesType', 'Outcome'
]

def map_and_normalize(df):
    """
    Map columns from various sources to the unified structure and normalize units.
    """
    col_map = {
        'age': 'Age', 'Age': 'Age',
        'sex': 'Gender', 'gender': 'Gender', 'Gender': 'Gender',
        'bmi': 'BMI', 'BMI': 'BMI',
        'weight': 'Weight', 'Weight': 'Weight',
        'height': 'Height', 'Height': 'Height',
        'hba1c': 'HbA1c', 'HbA1c': 'HbA1c', 'A1C': 'HbA1c',
        'physicalactivity': 'PhysicalActivity', 'PhysicalActivity': 'PhysicalActivity',
        'dietaryhabits': 'DietaryHabits', 'DietaryHabits': 'DietaryHabits',
        'familyhistory': 'FamilyHistory', 'FamilyHistory': 'FamilyHistory',
        'existingconditions': 'ExistingConditions', 'ExistingConditions': 'ExistingConditions',
        'diabetestype': 'DiabetesType', 'DiabetesType': 'DiabetesType',
        'outcome': 'Outcome', 'Outcome': 'Outcome', 'diabetes': 'Outcome', 'class': 'Outcome'
    }
    # Rename columns
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
    # Add missing columns
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = np.nan
    # Normalize units
    # Height: if in meters, convert to cm
    if df['Height'].max() < 10:
        df['Height'] = df['Height'] * 100
    # Weight: if in pounds, convert to kg
    if df['Weight'].max() > 200:
        df['Weight'] = df['Weight'] * 0.453592
    # Gender normalization
    df['Gender'] = df['Gender'].replace({'M': 'Male', 'F': 'Female', 1: 'Male', 0: 'Female'}).fillna('Unknown')
    # FamilyHistory normalization
    df['FamilyHistory'] = df['FamilyHistory'].replace({1: 'Yes', 0: 'No', 'Y': 'Yes', 'N': 'No'}).fillna('Unknown')
    # DiabetesType normalization
    df['DiabetesType'] = df['DiabetesType'].replace({np.nan: 'None'}).fillna('None')
    # Outcome normalization
    df['Outcome'] = df['Outcome'].replace({'Yes': 1, 'No': 0, 'Positive': 1, 'Negative': 0}).fillna(0).astype(int)
    # Fill missing values with median or 'Unknown'
    for col in ['Age', 'BMI', 'Weight', 'Height', 'HbA1c', 'PhysicalActivity']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(df[col].median())
    for col in ['DietaryHabits', 'ExistingConditions']:
        df[col] = df[col].fillna('Unknown')
    # Reorder columns
    df = df[COLUMNS]
    return df

def main():
    data_dir = 'data_sources/'
    all_files = glob.glob(os.path.join(data_dir, '*.csv'))
    dfs = []
    for file in all_files:
        print(f'Reading {file}')
        df = pd.read_csv(file)
        df = map_and_normalize(df)
        dfs.append(df)
    if not dfs:
        print('No CSV files found in data_sources/.')
        return
    merged = pd.concat(dfs, ignore_index=True)
    merged.to_csv('diabetes.csv', index=False)
    print(f'Merged dataset saved as diabetes.csv with {len(merged)} rows.')

if __name__ == '__main__':
    main() 