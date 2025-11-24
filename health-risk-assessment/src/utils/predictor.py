"""
Prediction utilities for the Diabetes Risk Assessment application
"""
import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config


def make_prediction(model, preprocessor, user_inputs):
    """
    Make diabetes risk prediction based on user inputs
    
    Args:
        model: Trained ML model
        preprocessor: Feature preprocessor (optional)
        user_inputs: Dictionary of user input values
        
    Returns:
        tuple: (prediction, probability_array)
            - prediction: Binary prediction (0 or 1)
            - probability_array: [prob_no_diabetes, prob_diabetes]
    """
    try:
        # Ensure features are in correct order
        ordered_inputs = [user_inputs[feature] for feature in config.FEATURE_NAMES]
        
        # Convert to DataFrame
        input_df = pd.DataFrame([ordered_inputs], columns=config.FEATURE_NAMES)
        
        # Apply preprocessing if available
        if preprocessor is not None:
            input_array = preprocessor.transform(input_df)
        else:
            input_array = input_df.values
        
        # Make prediction
        prediction = model.predict(input_array)[0]
        probability = model.predict_proba(input_array)[0]
        
        return int(prediction), probability
        
    except Exception as e:
        raise Exception(f"Error making prediction: {str(e)}")


def get_risk_level(probability):
    """
    Categorize risk level based on probability of diabetes
    
    Args:
        probability: Array [prob_no_diabetes, prob_diabetes]
        
    Returns:
        tuple: (risk_level, risk_color, risk_percentage)
    """
    risk_prob = probability[1] * 100  # Probability of diabetes in percentage
    
    if probability[1] < config.LOW_RISK_THRESHOLD:
        return "Low Risk", config.RISK_COLORS['low'], risk_prob
    elif probability[1] < config.HIGH_RISK_THRESHOLD:
        return "Moderate Risk", config.RISK_COLORS['moderate'], risk_prob
    else:
        return "High Risk", config.RISK_COLORS['high'], risk_prob


def format_probability(probability):
    """
    Format probability for display
    
    Args:
        probability: Array [prob_no_diabetes, prob_diabetes]
        
    Returns:
        dict: Formatted probabilities
    """
    return {
        'no_diabetes': f"{probability[0] * 100:.1f}%",
        'diabetes': f"{probability[1] * 100:.1f}%",
        'no_diabetes_raw': probability[0],
        'diabetes_raw': probability[1]
    }


def get_risk_interpretation(risk_level, risk_percentage):
    """
    Get interpretation text for the risk level
    
    Args:
        risk_level: String indicating risk level
        risk_percentage: Numeric risk percentage
        
    Returns:
        str: Interpretation text
    """
    interpretations = {
        "Low Risk": f"""
        Based on the information provided, your diabetes risk is **low ({risk_percentage:.1f}%)**.
        
        This means you have a relatively low probability of developing diabetes. However, 
        maintaining healthy lifestyle choices is important for continued wellness.
        """,
        
        "Moderate Risk": f"""
        Based on the information provided, your diabetes risk is **moderate ({risk_percentage:.1f}%)**.
        
        You may benefit from lifestyle modifications and regular health monitoring. 
        Consider consulting with a healthcare provider about preventive measures.
        """,
        
        "High Risk": f"""
        Based on the information provided, your diabetes risk is **high ({risk_percentage:.1f}%)**.
        
        **⚠️ We strongly recommend consulting with a healthcare provider** for proper evaluation 
        and personalized medical advice. Early intervention can significantly reduce complications.
        """
    }
    
    return interpretations.get(risk_level, "Unable to determine risk interpretation.")
