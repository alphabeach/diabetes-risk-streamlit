"""
Configuration settings for the Diabetes Risk Assessment application
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Model paths
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "gradient_boosting_model.pkl"
PREPROCESSOR_PATH = MODEL_DIR / "preprocessor2.pkl"

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "anthropic/claude-3.5-sonnet"

# Data paths
DATA_DIR = BASE_DIR / "src" / "data"
HEALTH_TIPS_PATH = DATA_DIR / "health_tips.json"

# Feature names from diabetes2.csv (21 features - excluding Diabetes_binary target)
FEATURE_NAMES = [
    'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker',
    'Stroke', 'HeartDiseaseorAttack', 'PhysActivity', 'Fruits',
    'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost',
    'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex',
    'Age', 'Education', 'Income'
]

# Feature labels for user-friendly display
FEATURE_LABELS = {
    'HighBP': 'High Blood Pressure',
    'HighChol': 'High Cholesterol',
    'CholCheck': 'Cholesterol Check in Past 5 Years',
    'BMI': 'Body Mass Index (BMI)',
    'Smoker': 'Have you smoked at least 100 cigarettes in your lifetime?',
    'Stroke': 'Ever had a Stroke',
    'HeartDiseaseorAttack': 'Coronary Heart Disease or Heart Attack',
    'PhysActivity': 'Physical Activity in Past 30 Days',
    'Fruits': 'Consume Fruit 1+ times per day',
    'Veggies': 'Consume Vegetables 1+ times per day',
    'HvyAlcoholConsump': 'Heavy Alcohol Consumption',
    'AnyHealthcare': 'Have Any Healthcare Coverage',
    'NoDocbcCost': 'Could not see doctor due to cost in past 12 months',
    'GenHlth': 'General Health',
    'MentHlth': 'Days of Poor Mental Health (past 30 days)',
    'PhysHlth': 'Days of Physical Illness/Injury (past 30 days)',
    'DiffWalk': 'Difficulty Walking or Climbing Stairs',
    'Sex': 'Sex',
    'Age': 'Age Category',
    'Education': 'Education Level',
    'Income': 'Income Level'
}

# Input ranges and options for numeric fields
INPUT_RANGES = {
    'BMI': {'min': 10.0, 'max': 70.0, 'default': 25.0, 'step': 0.1},
    'GenHlth': {'min': 1, 'max': 5, 'default': 3},
    'MentHlth': {'min': 0, 'max': 30, 'default': 0},
    'PhysHlth': {'min': 0, 'max': 30, 'default': 0},
    'Age': {'min': 1, 'max': 13, 'default': 7},
    'Education': {'min': 1, 'max': 6, 'default': 4},
    'Income': {'min': 1, 'max': 8, 'default': 5}
}

# Categorical mappings
AGE_CATEGORIES = {
    1: '18-24', 2: '25-29', 3: '30-34', 4: '35-39', 5: '40-44',
    6: '45-49', 7: '50-54', 8: '55-59', 9: '60-64', 10: '65-69',
    11: '70-74', 12: '75-79', 13: '80+'
}

EDUCATION_LEVELS = {
    1: 'Never attended/Kindergarten only',
    2: 'Grades 1-8',
    3: 'Grades 9-11',
    4: 'Grade 12/GED',
    5: 'College 1-3 years',
    6: 'College 4+ years'
}

INCOME_LEVELS = {
    1: '<₱10,000/month', 2: '₱10,000-₱20,000/month', 3: '₱20,000-₱30,000/month',
    4: '₱30,000-₱40,000/month', 5: '₱40,000-₱60,000/month', 6: '₱60,000-₱80,000/month',
    7: '₱80,000-₱100,000/month', 8: '₱100,000+/month'
}

GENERAL_HEALTH_LEVELS = {
    1: 'Excellent', 2: 'Very Good', 3: 'Good', 4: 'Fair', 5: 'Poor'
}

# App settings
APP_TITLE = "🏥 Diabetes Risk Assessment Tool"
APP_DESCRIPTION = "AI-powered diabetes risk prediction with personalized insights"
RISK_THRESHOLD = 0.5
LOW_RISK_THRESHOLD = 0.3
HIGH_RISK_THRESHOLD = 0.6

# Styling
RISK_COLORS = {
    'low': '#28a745',
    'moderate': '#ffc107',
    'high': '#dc3545'
}

# Population averages (will be calculated from dataset)
POPULATION_STATS = {
    'diabetic': {},
    'non_diabetic': {}
}
