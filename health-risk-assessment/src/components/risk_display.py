"""
Risk display component for showing prediction results
"""
import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config


def display_risk_assessment(risk_level, risk_percentage, probability, prediction):
    """
    Display the main risk assessment results with visual indicators
    
    Args:
        risk_level: String indicating risk level (Low/Moderate/High Risk)
        risk_percentage: Numeric risk percentage
        probability: Array [prob_no_diabetes, prob_diabetes]
        prediction: Binary prediction (0 or 1)
    """
    st.markdown("---")
    st.header("🎯 Your Diabetes Risk Assessment")
    
    # Get risk color
    risk_color = config.RISK_COLORS.get(risk_level.split()[0].lower(), '#000000')
    
    # Main risk display
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f"### Risk Level")
        st.markdown(f"<h1 style='color: {risk_color};'>{risk_level}</h1>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ")
        st.markdown("<br>", unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"### Risk Probability")
        st.markdown(f"<h1 style='color: {risk_color};'>{risk_percentage:.1f}%</h1>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Probability gauge chart
    display_probability_gauge(risk_percentage, risk_color)
    
    # Probability breakdown
    st.markdown("### 📊 Detailed Probability")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="No Diabetes Risk",
            value=f"{probability[0] * 100:.1f}%",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Diabetes Risk",
            value=f"{probability[1] * 100:.1f}%",
            delta=None
        )


def display_probability_gauge(risk_percentage, risk_color):
    """
    Display a gauge chart showing risk probability
    
    Args:
        risk_percentage: Numeric risk percentage
        risk_color: Color for the gauge
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Diabetes Risk Probability", 'font': {'size': 24}},
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': risk_color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#E8F5E9'},
                {'range': [30, 60], 'color': '#FFF3E0'},
                {'range': [60, 100], 'color': '#FFEBEE'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_risk_interpretation(risk_level, risk_percentage):
    """
    Display interpretation and explanation of the risk level
    
    Args:
        risk_level: String indicating risk level
        risk_percentage: Numeric risk percentage
    """
    st.markdown("### 📖 What Does This Mean?")
    
    interpretations = {
        "Low Risk": {
            "emoji": "✅",
            "message": f"""
Your diabetes risk assessment indicates a **low probability ({risk_percentage:.1f}%)** of developing diabetes 
based on your current health profile.

**What this means:**
- Your current lifestyle and health indicators suggest good metabolic health
- You are at lower risk compared to the general population
- Continue maintaining your healthy habits

**Important Note:** This is a risk estimate, not a diagnosis. Regular health check-ups are still recommended.
            """
        },
        "Moderate Risk": {
            "emoji": "⚠️",
            "message": f"""
Your diabetes risk assessment indicates a **moderate probability ({risk_percentage:.1f}%)** of developing diabetes 
based on your current health profile.

**What this means:**
- You have several risk factors that could increase your diabetes risk
- Lifestyle modifications can significantly reduce your risk
- Preventive measures are highly recommended

**Action Required:** Consider scheduling a check-up with your healthcare provider to discuss prevention strategies.
            """
        },
        "High Risk": {
            "emoji": "🚨",
            "message": f"""
Your diabetes risk assessment indicates a **high probability ({risk_percentage:.1f}%)** of developing diabetes 
based on your current health profile.

**What this means:**
- Multiple significant risk factors have been identified
- Early intervention is crucial to prevent or delay diabetes onset
- Medical evaluation is strongly recommended

**⚠️ URGENT ACTION REQUIRED:** Please schedule an appointment with a healthcare provider as soon as possible 
for comprehensive evaluation, blood work, and personalized treatment plan.
            """
        }
    }
    
    result = interpretations.get(risk_level, {
        "emoji": "ℹ️",
        "message": "Unable to determine risk interpretation."
    })
    
    st.markdown(f"{result['emoji']} {result['message']}")


def display_comparison_info():
    """Display information about how results compare to population averages"""
    st.markdown("### 📊 Understanding Your Risk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Risk Thresholds:**
        - 🟢 **Low Risk:** < 30%
        - 🟡 **Moderate Risk:** 30% - 60%
        - 🔴 **High Risk:** > 60%
        """)
    
    with col2:
        st.warning("""
        **Important Reminder:**
        - This is a screening tool, not a diagnostic test
        - Results are based on statistical models
        - Always consult healthcare professionals
        """)


def display_disclaimer():
    """Display important disclaimer about the assessment"""
    st.markdown("---")
    st.markdown("### ⚠️ Important Disclaimer")
    
    st.warning("""
    **Please Read Carefully:**
    
    This diabetes risk assessment tool is designed for **informational and educational purposes only**. 
    It is NOT a substitute for professional medical advice, diagnosis, or treatment.
    
    - This tool uses machine learning models trained on population health data
    - Individual health situations vary and may not be fully captured by this assessment
    - A high-risk result does NOT mean you have diabetes
    - A low-risk result does NOT guarantee you won't develop diabetes
    
    **Always seek the advice of your physician or other qualified health provider** with any questions 
    you may have regarding a medical condition. Never disregard professional medical advice or delay 
    in seeking it because of something you have read or results from this tool.
    
    If you think you may have a medical emergency, call your doctor or emergency services immediately.
    """)
