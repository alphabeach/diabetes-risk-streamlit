import streamlit as st
from components.assessment_form import render_assessment_form
from components.risk_calculator import calculate_risk
from components.results_display import display_results

def main():
    st.title("Health Risk Assessment")
    st.sidebar.header("User Input")

    user_data = render_assessment_form()

    if user_data:
        risk_prediction, probability_score = calculate_risk(user_data)
        display_results(risk_prediction, probability_score)

if __name__ == "__main__":
    main()