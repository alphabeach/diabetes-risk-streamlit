"""
Input form component for collecting user health data
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config


def render_input_form():
    """
    Render the comprehensive user input form for health data collection
    
    Returns:
        dict: Dictionary containing all user inputs with feature names as keys and user info
    """
    st.header("📋 Enter Your Health Information")
    st.markdown("Please provide accurate information for the best risk assessment.")
    st.markdown("---")
    
    # User Information Section
    st.subheader("👤 Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        user_name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
            help="Your name will be saved with your assessment history"
        )
    
    with col2:
        user_email = st.text_input(
            "Email Address",
            placeholder="your.email@example.com",
            help="Optional: Provide email to retrieve your assessment history later"
        )
    
    st.markdown("---")
    
    user_inputs = {}
    user_info = {
        'name': user_name if user_name else 'Anonymous',
        'email': user_email if user_email else ''
    }
    
    # ========== MEDICAL HISTORY ==========
    st.subheader("🩺 Medical History")
    col1, col2 = st.columns(2)
    
    with col1:
        user_inputs['HighBP'] = float(st.checkbox(
            config.FEATURE_LABELS['HighBP'],
            help="Have you been told by a healthcare professional that you have high blood pressure?"
        ))
        
        user_inputs['HighChol'] = float(st.checkbox(
            config.FEATURE_LABELS['HighChol'],
            help="Have you been told by a healthcare professional that you have high cholesterol?"
        ))
        
        user_inputs['CholCheck'] = float(st.checkbox(
            config.FEATURE_LABELS['CholCheck'],
            value=True,
            help="Have you had your cholesterol checked in the past 5 years?"
        ))
    
    with col2:
        user_inputs['Stroke'] = float(st.checkbox(
            config.FEATURE_LABELS['Stroke'],
            help="Have you ever been told you had a stroke?"
        ))
        
        user_inputs['HeartDiseaseorAttack'] = float(st.checkbox(
            config.FEATURE_LABELS['HeartDiseaseorAttack'],
            help="Have you ever been told you have coronary heart disease or myocardial infarction?"
        ))
        
        user_inputs['DiffWalk'] = float(st.checkbox(
            config.FEATURE_LABELS['DiffWalk'],
            help="Do you have serious difficulty walking or climbing stairs?"
        ))
    
    st.markdown("---")
    
    # ========== HEALTH METRICS ==========
    st.subheader("📊 Health Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        # BMI
        user_inputs['BMI'] = st.number_input(
            config.FEATURE_LABELS['BMI'],
            min_value=config.INPUT_RANGES['BMI']['min'],
            max_value=config.INPUT_RANGES['BMI']['max'],
            value=config.INPUT_RANGES['BMI']['default'],
            step=config.INPUT_RANGES['BMI']['step'],
            help="Body Mass Index = weight(kg) / height(m)². You can calculate it using online BMI calculators."
        )
        
        # General Health
        user_inputs['GenHlth'] = st.select_slider(
            config.FEATURE_LABELS['GenHlth'],
            options=list(range(1, 6)),
            value=config.INPUT_RANGES['GenHlth']['default'],
            format_func=lambda x: config.GENERAL_HEALTH_LEVELS[x],
            help="How would you rate your general health?"
        )
    
    with col2:
        # Mental Health Days
        user_inputs['MentHlth'] = st.slider(
            config.FEATURE_LABELS['MentHlth'],
            min_value=config.INPUT_RANGES['MentHlth']['min'],
            max_value=config.INPUT_RANGES['MentHlth']['max'],
            value=config.INPUT_RANGES['MentHlth']['default'],
            step=1,
            help="Thinking about your mental health, which includes stress, depression, and problems with emotions, for how many days during the past 30 days was your mental health not good?"
        )
        
        # Physical Health Days
        user_inputs['PhysHlth'] = st.slider(
            config.FEATURE_LABELS['PhysHlth'],
            min_value=config.INPUT_RANGES['PhysHlth']['min'],
            max_value=config.INPUT_RANGES['PhysHlth']['max'],
            value=config.INPUT_RANGES['PhysHlth']['default'],
            step=1,
            help="Thinking about your physical health, which includes physical illness and injury, for how many days during the past 30 days was your physical health not good?"
        )
    
    st.markdown("---")
    
    # ========== LIFESTYLE FACTORS ==========
    st.subheader("🏃 Lifestyle Factors")
    col1, col2 = st.columns(2)
    
    with col1:
        user_inputs['Smoker'] = float(st.checkbox(
            config.FEATURE_LABELS['Smoker'],
            help="Have you smoked at least 100 cigarettes (5 packs) in your entire life?"
        ))
        
        user_inputs['PhysActivity'] = float(st.checkbox(
            config.FEATURE_LABELS['PhysActivity'],
            value=True,
            help="Have you engaged in physical activity or exercise during the past 30 days (not including job)?"
        ))
        
        user_inputs['Fruits'] = float(st.checkbox(
            config.FEATURE_LABELS['Fruits'],
            value=True,
            help="Do you consume fruit 1 or more times per day?"
        ))
    
    with col2:
        user_inputs['Veggies'] = float(st.checkbox(
            config.FEATURE_LABELS['Veggies'],
            value=True,
            help="Do you consume vegetables 1 or more times per day?"
        ))
        
        user_inputs['HvyAlcoholConsump'] = float(st.checkbox(
            config.FEATURE_LABELS['HvyAlcoholConsump'],
            help="Heavy drinkers: adult men having more than 14 drinks per week and adult women having more than 7 drinks per week"
        ))
    
    st.markdown("---")
    
    # ========== HEALTHCARE ACCESS ==========
    st.subheader("🏥 Healthcare Access")
    col1, col2 = st.columns(2)
    
    with col1:
        user_inputs['AnyHealthcare'] = float(st.checkbox(
            config.FEATURE_LABELS['AnyHealthcare'],
            value=True,
            help="Do you have any kind of healthcare coverage, including health insurance, prepaid plans, or government plans?"
        ))
    
    with col2:
        user_inputs['NoDocbcCost'] = float(st.checkbox(
            config.FEATURE_LABELS['NoDocbcCost'],
            help="Was there a time in the past 12 months when you needed to see a doctor but could not because of cost?"
        ))
    
    st.markdown("---")
    
    # ========== DEMOGRAPHICS ==========
    st.subheader("👤 Demographics")
    col1, col2 = st.columns(2)
    
    with col1:
        # Sex
        user_inputs['Sex'] = float(st.radio(
            config.FEATURE_LABELS['Sex'],
            options=[0, 1],
            format_func=lambda x: '👩 Female' if x == 0 else '👨 Male',
            horizontal=True
        ))
        
        # Age
        user_inputs['Age'] = float(st.selectbox(
            config.FEATURE_LABELS['Age'],
            options=list(range(1, 14)),
            index=config.INPUT_RANGES['Age']['default'] - 1,
            format_func=lambda x: config.AGE_CATEGORIES[x]
        ))
    
    with col2:
        # Education
        user_inputs['Education'] = float(st.selectbox(
            config.FEATURE_LABELS['Education'],
            options=list(range(1, 7)),
            index=config.INPUT_RANGES['Education']['default'] - 1,
            format_func=lambda x: config.EDUCATION_LEVELS[x]
        ))
        
        # Income
        user_inputs['Income'] = float(st.selectbox(
            config.FEATURE_LABELS['Income'],
            options=list(range(1, 9)),
            index=config.INPUT_RANGES['Income']['default'] - 1,
            format_func=lambda x: config.INCOME_LEVELS[x]
        ))
    
    return user_inputs, user_info


def display_input_summary(user_inputs):
    """
    Display a summary of user inputs in an organized format
    
    Args:
        user_inputs: Dictionary of user input values
    """
    st.subheader("📝 Your Input Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Health Conditions**")
        conditions = ['HighBP', 'HighChol', 'Stroke', 'HeartDiseaseorAttack']
        for feature in conditions:
            value = "✅ Yes" if user_inputs[feature] == 1 else "❌ No"
            st.text(f"{config.FEATURE_LABELS[feature][:20]}...: {value}")
    
    with col2:
        st.markdown("**Lifestyle**")
        st.text(f"BMI: {user_inputs['BMI']:.1f}")
        st.text(f"Smoker: {'Yes' if user_inputs['Smoker'] == 1 else 'No'}")
        st.text(f"Physical Activity: {'Yes' if user_inputs['PhysActivity'] == 1 else 'No'}")
        st.text(f"General Health: {config.GENERAL_HEALTH_LEVELS[int(user_inputs['GenHlth'])]}")
    
    with col3:
        st.markdown("**Demographics**")
        st.text(f"Sex: {'Male' if user_inputs['Sex'] == 1 else 'Female'}")
        st.text(f"Age: {config.AGE_CATEGORIES[int(user_inputs['Age'])]}")
        st.text(f"Education: {config.EDUCATION_LEVELS[int(user_inputs['Education'])][:20]}...")
        st.text(f"Income: {config.INCOME_LEVELS[int(user_inputs['Income'])]}")
