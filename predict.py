import numpy as np
import pandas as pd
import joblib

# === Load trained model and preprocessor ===
MODEL_PATH = "models/Gradient_Boosting.pkl"
PREPROCESSOR_PATH = "models/preprocessor2.pkl"

print("🔄 Loading model and preprocessor...")
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)
print("✅ Model and preprocessor loaded successfully.\n")

questions = [
    ("HighBP", "Do you have high blood pressure? 0 = No, 1 = Yes: "),
    ("HighChol", "Do you have high cholesterol? 0 = No, 1 = Yes: "),
    ("CholCheck", "Have you checked your cholesterol in the last 5 years? 0 = No, 1 = Yes: "),
    ("BMI", "Enter your Body Mass Index (BMI): "),
    ("Smoker", "Have you smoked at least 100 cigarettes in your entire life (5 packs)? 0 = No, 1 = Yes: "),
    ("Stroke", "Have you ever had a stroke? 0 = No, 1 = Yes: "),
    ("HeartDiseaseorAttack", "Have you had coronary heart disease or myocardial infarction? 0 = No, 1 = Yes: "),
    ("PhysActivity", "Have you done physical activity in the past 30 days (not including job)? 0 = No, 1 = Yes: "),
    ("Fruits", "Do you consume fruit at least once per day? 0 = No, 1 = Yes: "),
    ("Veggies", "Do you consume vegetables at least once per day? 0 = No, 1 = Yes: "),
    ("HvyAlcoholConsump", "Are you a heavy drinker (Alcohol)? (Men >14 drinks/week, Women >7) 0 = No, 1 = Yes: "),
    ("AnyHealthcare", "Do you have any kind of health care coverage? 0 = No, 1 = Yes: "),
    ("NoDocbcCost", "Was there a time you needed to see a doctor but couldn't because of cost? 0 = No, 1 = Yes: "),
    ("GenHlth", "Rate your general health (1=Excellent, 2=Very Good, 3=Good, 4=Fair, 5=Poor): "),
    ("MentHlth", "How many days during the past 30 days was your mental health not good?: "),
    ("PhysHlth", "How many days during the past 30 days was your physical health not good?: "),
    ("DiffWalk", "Do you have serious difficulty walking or climbing stairs? 0 = No, 1 = Yes: "),
    ("Sex", "What is your sex? 0 = Female, 1 = Male: "),
    ("Age", "Select your age category (1=18-24, 2=25-29, 3=30-34, ..., 13=80+): "),
    ("Education", "Education level (1=No schooling, 2=Grades 1-8, 3=Grades 9-11, 4=High School Grad, 5=Some College, 6=College Grad): "),
    ("Income",  "Income category (1=Less than ₱120k, 2=₱120k–₱240k, 3=₱240k–₱480k, ""4=₱480k–₱720k, 5=₱720k–₱1M, 6=₱1M–₱1.5M, 7=₱1.5M–₱2M, 8=₱2M+): ")
]

inputs = {}
print("🩺 Please answer the following questions to estimate your prediabetes risk:\n")
for (feature, question) in questions:
    while True:
        try:
            value = float(input(question))
            inputs[feature] = value
            break
        except ValueError:
            print("⚠️ Invalid input. Please enter a numeric value (0, 1, or number).")

# Convert to DataFrame with correct column names
X_input = pd.DataFrame([inputs])
X_processed = preprocessor.transform(X_input)

probability = model.predict_proba(X_processed)[0][1]
risk_percent = probability * 100

print("\n🧮 Calculating your diabetes risk…")
print(f"\n📊 Your estimated risk score is: {risk_percent:.2f}%")

if risk_percent < 33.79:
    print("✅ Low risk — You are unlikely to have prediabetes/diabetes.")
elif risk_percent < 70.17:
    print("⚠️ Moderate risk — Your likelihood is moderate. Consider a check‑up and healthy lifestyle improvements.")
else:
    print("🚨 High risk — Your estimated chance is high. It is recommended to consult a doctor for further evaluation.")

print("\nThank you for using the Risk Predictor!")
