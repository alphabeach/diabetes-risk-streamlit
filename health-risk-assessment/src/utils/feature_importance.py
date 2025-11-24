"""
Feature importance and contribution analysis utilities
"""
import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config


def calculate_feature_importance(model, feature_names):
    """
    Extract feature importance from the model
    
    Args:
        model: Trained model with feature_importances_ attribute
        feature_names: List of feature names
        
    Returns:
        pd.DataFrame: Sorted DataFrame with features and importance scores
    """
    try:
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            
            # Create DataFrame
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': importances,
                'Feature_Label': [config.FEATURE_LABELS.get(f, f) for f in feature_names]
            })
            
            # Sort by importance
            importance_df = importance_df.sort_values('Importance', ascending=False)
            
            return importance_df
        else:
            return None
            
    except Exception as e:
        print(f"Error calculating feature importance: {str(e)}")
        return None


def get_user_risk_factors(user_inputs, feature_importance_df, top_n=5):
    """
    Identify the top risk factors for this specific user
    
    Args:
        user_inputs: Dictionary of user input values
        feature_importance_df: DataFrame with feature importance
        top_n: Number of top factors to return
        
    Returns:
        list: List of tuples (feature_label, user_value, importance, interpretation)
    """
    if feature_importance_df is None:
        return []
    
    risk_factors = []
    
    for _, row in feature_importance_df.head(top_n).iterrows():
        feature = row['Feature']
        feature_label = row['Feature_Label']
        importance = row['Importance']
        user_value = user_inputs.get(feature, None)
        
        if user_value is not None:
            # Format the value for display
            formatted_value = format_feature_value(feature, user_value)
            
            # Determine if this is a risk factor for the user
            is_risk = is_feature_risky(feature, user_value)
            
            risk_factors.append({
                'feature': feature,
                'label': feature_label,
                'value': formatted_value,
                'importance': importance,
                'is_risk': is_risk,
                'contribution': importance * 100  # Convert to percentage
            })
    
    return risk_factors


def format_feature_value(feature, value):
    """
    Format feature value for display
    
    Args:
        feature: Feature name
        value: Feature value
        
    Returns:
        str: Formatted value
    """
    # Binary features
    if feature in ['HighBP', 'HighChol', 'CholCheck', 'Smoker', 'Stroke', 
                   'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
                   'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'DiffWalk']:
        return "Yes" if value == 1 else "No"
    
    # Sex
    if feature == 'Sex':
        return "Male" if value == 1 else "Female"
    
    # Age
    if feature == 'Age':
        return config.AGE_CATEGORIES.get(int(value), f"Category {int(value)}")
    
    # Education
    if feature == 'Education':
        return config.EDUCATION_LEVELS.get(int(value), f"Level {int(value)}")
    
    # Income
    if feature == 'Income':
        return config.INCOME_LEVELS.get(int(value), f"Level {int(value)}")
    
    # General Health
    if feature == 'GenHlth':
        return config.GENERAL_HEALTH_LEVELS.get(int(value), f"Level {int(value)}")
    
    # Numeric features
    if feature == 'BMI':
        return f"{value:.1f}"
    
    if feature in ['MentHlth', 'PhysHlth']:
        return f"{int(value)} days"
    
    return str(value)


def is_feature_risky(feature, value):
    """
    Determine if a feature value indicates increased risk
    
    Args:
        feature: Feature name
        value: Feature value
        
    Returns:
        bool: True if risky, False otherwise
    """
    # High risk conditions (present = risky)
    high_risk_binary = ['HighBP', 'HighChol', 'Smoker', 'Stroke', 
                        'HeartDiseaseorAttack', 'HvyAlcoholConsump', 
                        'NoDocbcCost', 'DiffWalk']
    
    if feature in high_risk_binary:
        return value == 1
    
    # Protective factors (absent = risky)
    protective_binary = ['PhysActivity', 'Fruits', 'Veggies', 'AnyHealthcare', 'CholCheck']
    
    if feature in protective_binary:
        return value == 0
    
    # BMI
    if feature == 'BMI':
        return value >= 30  # Obese
    
    # General Health
    if feature == 'GenHlth':
        return value >= 4  # Fair or Poor
    
    # Mental/Physical Health Days
    if feature in ['MentHlth', 'PhysHlth']:
        return value >= 10  # 10+ days of poor health
    
    # Age (older = higher risk)
    if feature == 'Age':
        return value >= 9  # 60+
    
    # Default
    return False


def get_risk_factor_explanation(feature, value, importance):
    """
    Generate explanation for why a feature is a risk factor
    
    Args:
        feature: Feature name
        value: Feature value
        importance: Importance score
        
    Returns:
        str: Explanation text
    """
    explanations = {
        'HighBP': "High blood pressure is a major risk factor for diabetes and cardiovascular complications.",
        'HighChol': "High cholesterol levels are associated with increased diabetes risk.",
        'BMI': "Higher BMI (especially obesity) significantly increases diabetes risk.",
        'Smoker': "Smoking increases inflammation and insulin resistance.",
        'Stroke': "Previous stroke indicates cardiovascular complications that often coexist with diabetes.",
        'HeartDiseaseorAttack': "Heart disease and diabetes share many risk factors and often occur together.",
        'PhysActivity': "Lack of physical activity reduces insulin sensitivity.",
        'Fruits': "Inadequate fruit consumption may indicate poor dietary habits.",
        'Veggies': "Low vegetable intake is associated with poor metabolic health.",
        'HvyAlcoholConsump': "Heavy alcohol use can affect blood sugar regulation.",
        'GenHlth': "Poor general health often correlates with metabolic dysfunction.",
        'Age': "Diabetes risk increases with age due to decreased insulin sensitivity.",
        'MentHlth': "Poor mental health can affect lifestyle choices and metabolic health.",
        'PhysHlth': "Physical health problems may limit activity and affect metabolism."
    }
    
    return explanations.get(feature, f"This factor contributes {importance*100:.1f}% to the overall risk assessment.")
