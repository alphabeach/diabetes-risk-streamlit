"""
Model loading utilities for the Diabetes Risk Assessment application
"""
import pickle
import joblib
import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config


@st.cache_resource
def load_model():
    """
    Load the trained Gradient Boosting model
    
    Returns:
        model: Trained scikit-learn model or None if error
    """
    try:
        model_path = config.MODEL_PATH
        if not model_path.exists():
            st.error(f"❌ Model file not found at {model_path}")
            st.info("Please ensure gradient_boosting_model.pkl is in the models/ directory")
            return None
        
        # Try loading with joblib first (common for sklearn models)
        try:
            model = joblib.load(model_path)
            st.success("✅ Model loaded successfully (joblib)")
            return model
        except:
            # If joblib fails, try pickle
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            st.success("✅ Model loaded successfully (pickle)")
            return model
        
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None


@st.cache_resource
def load_preprocessor():
    """
    Load the feature preprocessor/scaler if it exists
    
    Returns:
        preprocessor: Preprocessing object or None
    """
    try:
        preprocessor_path = config.PREPROCESSOR_PATH
        
        if not preprocessor_path.exists():
            st.warning("⚠️ No preprocessor found. Using raw features.")
            return None
        
        # Try loading with joblib first
        try:
            preprocessor = joblib.load(preprocessor_path)
            return preprocessor
        except:
            # If joblib fails, try pickle
            with open(preprocessor_path, 'rb') as f:
                preprocessor = pickle.load(f)
            return preprocessor
        
    except Exception as e:
        st.warning(f"⚠️ Could not load preprocessor: {str(e)}")
        return None


def verify_model_compatibility(model, feature_names):
    """
    Verify that the model is compatible with the expected features
    
    Args:
        model: Loaded model
        feature_names: List of expected feature names
        
    Returns:
        bool: True if compatible, False otherwise
    """
    try:
        # Check if model has the expected number of features
        if hasattr(model, 'n_features_in_'):
            expected_features = model.n_features_in_
            if len(feature_names) != expected_features:
                st.error(f"Feature mismatch: Model expects {expected_features} features, but {len(feature_names)} provided")
                return False
        
        return True
        
    except Exception as e:
        st.error(f"Error verifying model compatibility: {str(e)}")
        return False
