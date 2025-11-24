"""
Database utilities for storing and retrieving assessment history using CSV
Note: On Streamlit Cloud (read-only filesystem), saving is disabled gracefully
"""
import pandas as pd
import os
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config


# Database file path
DB_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DB_FILE = DB_DIR / "assessment_history.csv"


def is_cloud_environment():
    """
    Detect if running in Streamlit Cloud (read-only filesystem)
    
    Returns:
        bool: True if in cloud, False if local
    """
    # Check for common cloud environment indicators
    return (
        os.getenv('STREAMLIT_SHARING_MODE') is not None or
        os.getenv('HOSTNAME', '').startswith('streamlit') or
        not os.access(Path(__file__).resolve().parent.parent.parent, os.W_OK)
    )


def initialize_database():
    """
    Initialize the CSV database file if it doesn't exist
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create data directory if it doesn't exist
        DB_DIR.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists
        if not DB_FILE.exists():
            # Create empty DataFrame with columns
            df = pd.DataFrame(columns=[
                'user_id', 'timestamp', 'name', 'email', 'age_category', 'sex',
                'bmi', 'high_bp', 'high_chol', 'smoker', 'diabetes_risk',
                'risk_percentage', 'prediction'
            ])
            df.to_csv(DB_FILE, index=False)
            return True
        
        return True
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        return False


def save_assessment(user_data, risk_level, risk_percentage, prediction):
    """
    Save assessment results to CSV database (local only)
    On Streamlit Cloud, this gracefully skips saving due to read-only filesystem
    
    Args:
        user_data: Dictionary containing user information (name, email, inputs)
        risk_level: String indicating risk level
        risk_percentage: Numeric risk percentage
        prediction: Binary prediction (0 or 1)
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Skip saving in cloud environment (read-only filesystem)
    if is_cloud_environment():
        return False
    
    try:
        # Initialize database if needed
        initialize_database()
        
        # Read existing data
        if DB_FILE.exists() and os.path.getsize(DB_FILE) > 0:
            df = pd.read_csv(DB_FILE)
            user_id = len(df) + 1
        else:
            df = pd.DataFrame()
            user_id = 1
        
        # Prepare new record
        new_record = {
            'user_id': user_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'name': user_data.get('name', 'Anonymous'),
            'email': user_data.get('email', ''),
            'age_category': user_data['inputs'].get('Age', 0),
            'sex': user_data['inputs'].get('Sex', 0),
            'bmi': user_data['inputs'].get('BMI', 0),
            'high_bp': user_data['inputs'].get('HighBP', 0),
            'high_chol': user_data['inputs'].get('HighChol', 0),
            'smoker': user_data['inputs'].get('Smoker', 0),
            'diabetes_risk': risk_level,
            'risk_percentage': round(risk_percentage, 2),
            'prediction': prediction
        }
        
        # Append new record
        df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
        
        # Save to CSV
        df.to_csv(DB_FILE, index=False)
        
        return True
        
    except Exception as e:
        print(f"Error saving assessment: {str(e)}")
        return False


def get_all_assessments():
    """
    Retrieve all assessment records from CSV
    
    Returns:
        pd.DataFrame: DataFrame containing all assessments or empty DataFrame if error
    """
    try:
        if DB_FILE.exists() and os.path.getsize(DB_FILE) > 0:
            return pd.read_csv(DB_FILE)
        else:
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error retrieving assessments: {str(e)}")
        return pd.DataFrame()


def get_user_assessments(user_email):
    """
    Retrieve assessments for a specific user
    
    Args:
        user_email: Email address of the user
        
    Returns:
        pd.DataFrame: DataFrame containing user's assessments
    """
    try:
        df = get_all_assessments()
        if not df.empty:
            return df[df['email'] == user_email]
        return pd.DataFrame()
        
    except Exception as e:
        print(f"Error retrieving user assessments: {str(e)}")
        return pd.DataFrame()


def get_assessment_by_id(user_id):
    """
    Retrieve a specific assessment by ID
    
    Args:
        user_id: Unique ID of the assessment
        
    Returns:
        dict: Assessment record or None if not found
    """
    try:
        df = get_all_assessments()
        if not df.empty:
            record = df[df['user_id'] == user_id]
            if not record.empty:
                return record.iloc[0].to_dict()
        return None
        
    except Exception as e:
        print(f"Error retrieving assessment: {str(e)}")
        return None


def get_statistics():
    """
    Get statistics from all assessments
    
    Returns:
        dict: Statistics including counts, averages, etc.
    """
    try:
        df = get_all_assessments()
        
        if df.empty:
            return {
                'total_assessments': 0,
                'high_risk_count': 0,
                'moderate_risk_count': 0,
                'low_risk_count': 0,
                'average_bmi': 0,
                'average_age': 0
            }
        
        stats = {
            'total_assessments': len(df),
            'high_risk_count': len(df[df['diabetes_risk'] == 'High Risk']),
            'moderate_risk_count': len(df[df['diabetes_risk'] == 'Moderate Risk']),
            'low_risk_count': len(df[df['diabetes_risk'] == 'Low Risk']),
            'average_bmi': df['bmi'].mean(),
            'average_risk_percentage': df['risk_percentage'].mean(),
            'male_count': len(df[df['sex'] == 1]),
            'female_count': len(df[df['sex'] == 0]),
            'recent_assessments': df.tail(5).to_dict('records')
        }
        
        return stats
        
    except Exception as e:
        print(f"Error calculating statistics: {str(e)}")
        return {}


def delete_assessment(user_id):
    """
    Delete an assessment record
    
    Args:
        user_id: ID of the assessment to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        df = get_all_assessments()
        
        if not df.empty:
            df = df[df['user_id'] != user_id]
            df.to_csv(DB_FILE, index=False)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error deleting assessment: {str(e)}")
        return False


def export_to_excel(output_path):
    """
    Export assessment history to Excel file
    
    Args:
        output_path: Path for the Excel file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        df = get_all_assessments()
        
        if not df.empty:
            df.to_excel(output_path, index=False, engine='openpyxl')
            return True
        
        return False
        
    except Exception as e:
        print(f"Error exporting to Excel: {str(e)}")
        return False
