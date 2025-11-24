from streamlit import st
from utils.validators import validate_inputs

def render_assessment_form():
    st.title("Health Risk Assessment Form")

    # Collect user inputs
    age = st.number_input("Age", min_value=0, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", min_value=0.0)
    height = st.number_input("Height (cm)", min_value=0.0)
    smoking_status = st.selectbox("Smoking Status", ["Non-smoker", "Former smoker", "Current smoker"])
    exercise_frequency = st.selectbox("Exercise Frequency", ["None", "Occasionally", "Regularly"])

    # Validate inputs
    if st.button("Submit"):
        if validate_inputs(age, weight, height):
            # Process the inputs and pass them to the risk calculator
            st.success("Inputs are valid. Proceeding with risk assessment...")
            # Here you would call the risk calculator function
        else:
            st.error("Please correct the invalid inputs.")