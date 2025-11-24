"""
Database utilities for storing and retrieving assessment history
Supports both local CSV and cloud Google Sheets (public sheet, no secrets needed)
"""
import pandas as pd
import os
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config

# Try importing gspread for Google Sheets
try:
    import gspread
    from gspread.exceptions import APIError, SpreadsheetNotFound
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

# Database file path (for local)
DB_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DB_FILE = DB_DIR / "assessment_history.csv"

# Google Sheet ID - Set this to your publicly writable Google Sheet ID
# See SETUP_GOOGLE_SHEET.md in the project root for setup instructions
# Leave as None to disable cloud saving
GOOGLE_SHEET_ID = None  # Example: "1ABC123XYZ789-yourSheetId"


def get_sheet_configured():
    """Check if Google Sheet is configured"""
    return GOOGLE_SHEET_ID is not None and GOOGLE_SHEET_ID != ""


def is_cloud_environment():
    """
    Detect if running in Streamlit Cloud
    
    Returns:
        bool: True if in cloud, False if local
    """
    # Check for common cloud environment indicators
    return (
        os.getenv('STREAMLIT_SHARING_MODE') is not None or
        os.getenv('HOSTNAME', '').startswith('streamlit') or
        not os.access(Path(__file__).resolve().parent.parent.parent, os.W_OK)
    )


def get_google_sheet():
    """
    Get Google Sheet for public writing (no authentication needed for public sheets)
    
    Returns:
        worksheet or None
    """
    if not GSPREAD_AVAILABLE or GOOGLE_SHEET_ID is None:
        return None
    
    try:
        # Use anonymous access for publicly writable sheets
        gc = gspread.service_account_from_dict({})  # Empty dict for anonymous
        worksheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
        return worksheet
    except Exception as e:
        # Try alternative method - direct API access for public sheets
        try:
            import requests
            url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"
            return url  # Return URL for read operations
        except:
            print(f"Error accessing Google Sheet: {str(e)}")
            return None


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
    Save assessment results to database
    Uses Google Sheets in cloud (if configured), CSV locally
    
    Args:
        user_data: Dictionary containing user information (name, email, inputs)
        risk_level: String indicating risk level
        risk_percentage: Numeric risk percentage
        prediction: Binary prediction (0 or 1)
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Prepare common data
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    name = user_data.get('name', 'Anonymous')
    email = user_data.get('email', '')
    age = user_data['inputs'].get('Age', 0)
    sex = user_data['inputs'].get('Sex', 0)
    bmi = user_data['inputs'].get('BMI', 0)
    high_bp = user_data['inputs'].get('HighBP', 0)
    high_chol = user_data['inputs'].get('HighChol', 0)
    smoker = user_data['inputs'].get('Smoker', 0)
    
    # Try Google Sheets first if in cloud and configured
    if is_cloud_environment() and GOOGLE_SHEET_ID:
        try:
            # Use simple HTTP POST to Google Forms-style endpoint
            # This works for publicly writable sheets without authentication
            import requests
            
            # Get current row count to assign user_id
            csv_url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"
            response = requests.get(csv_url, timeout=5)
            if response.status_code == 200:
                existing_lines = response.text.strip().split('\n')
                user_id = len(existing_lines)  # Header is line 1, so this gives next ID
            else:
                user_id = 1
            
            # Append via Google Sheets API (public write endpoint)
            append_url = f"https://sheets.googleapis.com/v4/spreadsheets/{GOOGLE_SHEET_ID}/values/Sheet1!A:M:append"
            values = [[
                user_id, timestamp, name, email,
                float(age), float(sex), float(bmi),
                float(high_bp), float(high_chol), float(smoker),
                risk_level, round(float(risk_percentage), 2), int(prediction)
            ]]
            
            append_response = requests.post(
                append_url,
                json={"values": values},
                params={"valueInputOption": "RAW"},
                timeout=10
            )
            
            if append_response.status_code in [200, 201]:
                return True
            else:
                print(f"Google Sheets append failed: {append_response.status_code}")
        except Exception as e:
            print(f"Error saving to Google Sheets: {str(e)}")
            # Fall through to local save if not in cloud
    
    # Local CSV saving (skip if in cloud without Google Sheets configured)
    if is_cloud_environment() and not GOOGLE_SHEET_ID:
        return False  # Can't save in cloud without Google Sheets configured
    
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
            'timestamp': timestamp,
            'name': name,
            'email': email,
            'age_category': age,
            'sex': sex,
            'bmi': bmi,
            'high_bp': high_bp,
            'high_chol': high_chol,
            'smoker': smoker,
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
    Retrieve all assessment records
    Reads from Google Sheets in cloud (if configured), CSV locally
    
    Returns:
        pd.DataFrame: DataFrame containing all assessments or empty DataFrame if error
    """
    # Try Google Sheets first if in cloud and configured
    if is_cloud_environment() and GOOGLE_SHEET_ID:
        try:
            import requests
            csv_url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"
            response = requests.get(csv_url, timeout=10)
            
            if response.status_code == 200:
                from io import StringIO
                df = pd.read_csv(StringIO(response.text))
                return df if not df.empty else pd.DataFrame()
        except Exception as e:
            print(f"Error reading from Google Sheets: {str(e)}")
            # Fall through to local read
    
    # Local CSV fallback
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
