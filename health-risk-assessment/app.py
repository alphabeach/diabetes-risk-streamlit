"""
Diabetes Risk Assessment Tool - Main Streamlit Application

This application provides AI-powered diabetes risk prediction with personalized insights.
It includes:
1. Instant Risk Assessment
2. Personalized Risk Factor Analysis
3. Actionable Health Recommendations (AI-powered via OpenRouter API)
4. Downloadable Summary Report (PDF)
5. Comparison to Population Averages
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import configuration
import config

# Import utilities
from src.utils.model_loader import load_model, load_preprocessor
from src.utils.predictor import make_prediction, get_risk_level, format_probability
from src.utils.feature_importance import calculate_feature_importance, get_user_risk_factors
from src.utils.openrouter_client import generate_recommendations
from src.utils.pdf_generator import generate_pdf_report
from src.utils.database import save_assessment, get_statistics, is_cloud_environment, get_sheet_configured

# Import components
from src.components.input_form import render_input_form, display_input_summary
from src.components.risk_display import (
    display_risk_assessment, 
    display_risk_interpretation,
    display_comparison_info,
    display_disclaimer
)
from src.components.factor_analysis import (
    display_feature_importance,
    display_user_risk_factors,
    display_factor_comparison
)
from src.components.recommendations import (
    display_recommendations,
    display_lifestyle_tips,
    display_resources
)
from src.components.admin_dashboard import display_admin_dashboard


def main():
    """Main application function"""
    
    # Page configuration
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS styling
    st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        .stAlert {
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        h1 {
            color: #2C3E50;
            padding-bottom: 1rem;
        }
        h2 {
            color: #34495E;
            padding-top: 1rem;
        }
        .stButton>button {
            width: 100%;
            background-color: #3498DB;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #2980B9;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'assessment_complete' not in st.session_state:
        st.session_state.assessment_complete = False
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        
        # Navigation menu - show Admin Dashboard only if logged in as admin
        nav_options = ["🏠 Home", "📋 Assessment", "ℹ️ About"]
        if st.session_state.is_admin:
            nav_options.insert(2, "📊 Admin Dashboard")
        
        page = st.radio(
            "Go to:",
            nav_options,
            index=1 if not st.session_state.assessment_complete else 1
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        show_debug = st.checkbox("Show Debug Info", value=False)
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        
        # Show different stats based on environment
        if is_cloud_environment():
            # Cloud mode - check if Google Sheets is configured
            if get_sheet_configured():
                try:
                    stats = get_statistics()
                    if stats and stats.get('total_assessments', 0) > 0:
                        st.info(f"""
                        **Total Assessments:** {stats['total_assessments']}
                        
                        **High Risk:** {stats['high_risk_count']}
                        
                        **Moderate Risk:** {stats['moderate_risk_count']}
                        
                        **Low Risk:** {stats['low_risk_count']}
                        
                        💾 *Saved to Google Sheets*
                        """)
                    else:
                        st.info("""
                        **Features Analyzed:** 21
                        
                        **Model:** Gradient Boosting
                        
                        💾 *Cloud saving enabled*
                        """)
                except:
                    st.info("""
                    **Features Analyzed:** 21
                    
                    **Model:** Gradient Boosting
                    
                    💾 *Cloud saving enabled*
                    """)
            else:
                st.info("""
                **Features Analyzed:** 21
                
                **Model:** Gradient Boosting
                
                ℹ️ *Cloud saving disabled*
                
                See `SETUP_GOOGLE_SHEET.md` to enable
                """)
        else:
            # Local mode - try to show saved stats
            try:
                stats = get_statistics()
                if stats and stats.get('total_assessments', 0) > 0:
                    st.info(f"""
                    **Total Assessments:** {stats['total_assessments']}
                    
                    **High Risk:** {stats['high_risk_count']}
                    
                    **Moderate Risk:** {stats['moderate_risk_count']}
                    
                    **Low Risk:** {stats['low_risk_count']}
                    """)
                else:
                    st.info("""
                    **Features Analyzed:** 21
                    
                    **Model:** Gradient Boosting
                    
                    **Accuracy:** High performance on validation data
                    """)
            except:
                st.info("""
                **Features Analyzed:** 21
                
                **Model:** Gradient Boosting
                
                **Accuracy:** High performance on validation data
                """)
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.success("""
        - Provide accurate information
        - Complete all fields
        - Consult healthcare provider for medical advice
        """)
        
        # Hidden admin access at the bottom - no label
        st.markdown("---")
        st.markdown("")  # Empty space
        admin_key = st.text_input("", type="password", key="admin_access", 
                                   label_visibility="collapsed")
        if admin_key == "admin123":  # Change this to a secure password
            if not st.session_state.is_admin:
                st.session_state.is_admin = True
                st.rerun()
        
        if st.session_state.is_admin:
            st.success("✓ Admin")
            if st.button("Logout", key="admin_logout"):
                st.session_state.is_admin = False
                st.rerun()
    # Main content area
    if page == "🏠 Home":
        display_home_page()
    elif page == "📋 Assessment":
        display_assessment_page(show_debug)
    elif page == "📊 Admin Dashboard":
        display_admin_dashboard()
    elif page == "ℹ️ About":
        display_about_page()


def display_home_page():
    """Display the home/welcome page"""
    st.title(config.APP_TITLE)
    st.markdown(f"### {config.APP_DESCRIPTION}")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Instant Assessment")
        st.write("Get immediate diabetes risk prediction with probability scores based on your health data.")
    
    with col2:
        st.markdown("### 📊 Personal Analysis")
        st.write("Understand which factors contribute most to your risk with detailed explanations.")
    
    with col3:
        st.markdown("### 💡 Smart Recommendations")
        st.write("Receive AI-powered, personalized health recommendations tailored to your risk profile.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 PDF Reports")
        st.write("Download comprehensive summary reports to share with your healthcare provider.")
    
    with col2:
        st.markdown("### 📈 Population Comparison")
        st.write("See how your metrics compare to diabetic and non-diabetic population averages.")
    
    st.markdown("---")
    
    st.info("""
    ### 🚀 Get Started
    
    Click on **📋 Assessment** in the sidebar to begin your diabetes risk assessment.
    
    The assessment takes approximately 5-10 minutes to complete and covers:
    - Medical history
    - Health metrics
    - Lifestyle factors
    - Demographics
    """)
    
    st.warning("""
    ### ⚠️ Important Notice
    
    This tool is for **educational and informational purposes only**. It is NOT a substitute for 
    professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare 
    professionals regarding any medical concerns.
    """)


def display_assessment_page(show_debug):
    """Display the main assessment page"""
    st.title("📋 Diabetes Risk Assessment")
    st.markdown("Complete the form below to receive your personalized risk assessment.")
    
    # Load model and preprocessor
    with st.spinner("Loading prediction model..."):
        model = load_model()
        preprocessor = load_preprocessor()
    
    if model is None:
        st.error("❌ Unable to load the prediction model. Please check that the model file exists in the models/ directory.")
        return
    
    # Render input form
    user_inputs, user_info = render_input_form()
    
    st.markdown("---")
    
    # Assessment button
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        assess_button = st.button("🔍 Analyze Risk", type="primary", use_container_width=True)
    
    # Process assessment
    if assess_button:
        with st.spinner("Analyzing your health data..."):
            try:
                # Make prediction
                prediction, probability = make_prediction(model, preprocessor, user_inputs)
                risk_level, risk_color, risk_percentage = get_risk_level(probability)
                
                # Calculate feature importance
                feature_importance_df = calculate_feature_importance(model, config.FEATURE_NAMES)
                risk_factors = get_user_risk_factors(user_inputs, feature_importance_df, top_n=10)
                
                # Store results in session state
                st.session_state.results = {
                    'user_inputs': user_inputs,
                    'user_info': user_info,
                    'prediction': prediction,
                    'probability': probability,
                    'risk_level': risk_level,
                    'risk_percentage': risk_percentage,
                    'risk_color': risk_color,
                    'feature_importance_df': feature_importance_df,
                    'risk_factors': risk_factors
                }
                st.session_state.assessment_complete = True
                
                # Save to database (only works locally, not on Streamlit Cloud)
                try:
                    user_data = {
                        'name': user_info['name'],
                        'email': user_info['email'],
                        'inputs': user_inputs
                    }
                    saved = save_assessment(user_data, risk_level, risk_percentage, prediction)
                    if not saved and is_cloud_environment():
                        # Don't show warning in cloud - it's expected behavior
                        pass
                except Exception as db_error:
                    # Silently handle save errors in production
                    if show_debug:
                        st.warning(f"Note: Assessment not saved to history: {str(db_error)}")
                
                st.success("✅ Assessment completed successfully!")
                
            except Exception as e:
                st.error(f"❌ Error during assessment: {str(e)}")
                if show_debug:
                    st.exception(e)
                return
    
    # Display results if assessment is complete
    if st.session_state.assessment_complete and st.session_state.results:
        display_results(st.session_state.results, show_debug)


def display_results(results, show_debug):
    """Display the assessment results"""
    st.markdown("---")
    st.markdown("## 📊 Your Results")
    
    # Extract results
    user_inputs = results['user_inputs']
    prediction = results['prediction']
    probability = results['probability']
    risk_level = results['risk_level']
    risk_percentage = results['risk_percentage']
    feature_importance_df = results['feature_importance_df']
    risk_factors = results['risk_factors']
    
    # 1. Display Risk Assessment
    display_risk_assessment(risk_level, risk_percentage, probability, prediction)
    
    # 2. Display Risk Interpretation
    display_risk_interpretation(risk_level, risk_percentage)
    
    # 3. Display Feature Analysis
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Your Risk Factors", "📊 Model Insights", "📈 Population Comparison"])
    
    with tab1:
        display_user_risk_factors(risk_factors)
    
    with tab2:
        display_feature_importance(feature_importance_df)
    
    with tab3:
        display_factor_comparison(user_inputs, config.POPULATION_STATS)
    
    # 4. Generate and Display Recommendations
    st.markdown("---")
    
    with st.spinner("Generating personalized recommendations..."):
        recommendations = generate_recommendations(
            user_inputs, 
            risk_level, 
            risk_percentage, 
            risk_factors
        )
    
    display_recommendations(recommendations, risk_level)
    
    # 5. Display Lifestyle Tips
    display_lifestyle_tips()
    
    # 6. Display Resources
    display_resources()
    
    # 7. PDF Download
    st.markdown("---")
    st.markdown("### 📄 Download Your Report")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("📥 Generate PDF Report", use_container_width=True):
            with st.spinner("Generating PDF report..."):
                try:
                    pdf_buffer = generate_pdf_report(
                        user_inputs,
                        prediction,
                        probability,
                        risk_level,
                        risk_percentage,
                        risk_factors
                    )
                    
                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=pdf_buffer,
                        file_name=f"diabetes_risk_assessment_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    st.success("✅ PDF report generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error generating PDF: {str(e)}")
                    if show_debug:
                        st.exception(e)
    
    # 8. Display Disclaimer
    display_disclaimer()
    
    # 9. Reset Button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🔄 Start New Assessment", use_container_width=True):
            st.session_state.assessment_complete = False
            st.session_state.results = None
            st.rerun()
    
    # Debug information
    if show_debug:
        st.markdown("---")
        st.markdown("### 🐛 Debug Information")
        
        with st.expander("View Raw Data"):
            st.json({
                'prediction': int(prediction),
                'probability': {
                    'no_diabetes': float(probability[0]),
                    'diabetes': float(probability[1])
                },
                'risk_level': risk_level,
                'risk_percentage': float(risk_percentage),
                'user_inputs': {k: float(v) for k, v in user_inputs.items()}
            })


def display_about_page():
    """Display the about page"""
    st.title("ℹ️ About This Tool")
    
    st.markdown("""
    ## Diabetes Risk Assessment Tool
    
    This application provides AI-powered diabetes risk prediction with personalized insights 
    to help individuals understand their diabetes risk and take preventive action.
    
    ### 🎯 Features
    
    1. **Instant Risk Assessment**
       - Machine learning-powered predictions
       - Probability scores and risk categorization
       - Based on 21 health and lifestyle factors
    
    2. **Personalized Risk Factor Analysis**
       - Identifies your specific risk factors
       - Explains why each factor matters
       - Compares your values to population averages
    
    3. **AI-Powered Recommendations**
       - Personalized health guidance (via OpenRouter API)
       - Evidence-based lifestyle tips
       - Action steps tailored to your risk level
    
    4. **Downloadable PDF Reports**
       - Comprehensive summary of your assessment
       - Share with healthcare providers
       - Track your progress over time
    
    5. **Population Comparisons**
       - See how your metrics compare to others
       - Understand your risk in context
       - Visualized with interactive charts
    
    ### 🤖 Technology
    
    - **Model:** Gradient Boosting Classifier
    - **Framework:** Streamlit
    - **AI Recommendations:** OpenRouter API (Claude, GPT-4, etc.)
    - **Visualization:** Plotly
    - **PDF Generation:** ReportLab
    
    ### 📊 Data & Privacy
    
    - No data is stored or transmitted to external servers
    - All processing happens locally in your browser session
    - Your privacy is fully protected
    - This tool does not diagnose medical conditions
    
    ### ⚠️ Disclaimer
    
    This tool is for educational and informational purposes only. It is NOT a substitute for 
    professional medical advice, diagnosis, or treatment. Always seek the advice of your 
    physician or other qualified health provider with any questions you may have regarding 
    a medical condition.
    
    ### 📚 References
    
    This tool is based on research and data from:
    - Centers for Disease Control and Prevention (CDC)
    - American Diabetes Association
    - National Institute of Diabetes and Digestive and Kidney Diseases
    - Behavioral Risk Factor Surveillance System (BRFSS)
    
    ### 👨‍💻 Development
    
    Developed as part of a capstone project to demonstrate the application of machine learning 
    in healthcare risk assessment and preventive medicine.
    
    ### 📞 Support
    
    For technical issues or questions about this tool, please consult your project documentation 
    or contact your healthcare provider for medical questions.
    """)
    
    st.markdown("---")
    st.info("**Version:** 1.0.0 | **Last Updated:** November 2025")


# Import pandas for timestamp (needed for PDF filename)
import pandas as pd


if __name__ == "__main__":
    main()
