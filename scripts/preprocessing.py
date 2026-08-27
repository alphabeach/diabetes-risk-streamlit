import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

# === Hardcoded path to your dataset ===
DATA_PATH = os.path.join(ROOT_DIR, "data", "diabetes2.csv")
OUTPUT_DIR = os.path.join(ROOT_DIR, "models")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Load the dataset ===
print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

print(f"✅ Dataset loaded successfully with shape: {df.shape}")
print("Columns:", list(df.columns))

# === Define target and features ===
TARGET = "Diabetes_binary"  # Changed from "Diabetes_012"
X = df.drop(columns=[TARGET])
y = df[TARGET]

# === Check for missing values ===
print("\nChecking for missing values...")
missing = X.isnull().sum()
if missing.any():
    print("⚠️ Missing values found — filling with median values.")
    X = X.fillna(X.median())
else:
    print("✅ No missing values detected.")

# === Identify numeric and categorical features ===
# (All are numeric in your dataset, but we keep structure flexible)
numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()

# === Create preprocessing pipeline ===
numeric_transformer = Pipeline(steps=[
    ("scaler", StandardScaler())
])

# If you have categorical columns later, you can add encoding here
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features)
    ],
    remainder="passthrough"
)

# === Split the dataset ===
print("\nSplitting dataset into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"✅ Training set: {X_train.shape}, Testing set: {X_test.shape}")

# === Fit the preprocessor on training data ===
print("\nFitting preprocessor...")
preprocessor.fit(X_train)
print("✅ Preprocessing complete!")

# === Save preprocessor and processed datasets ===
joblib.dump(preprocessor, os.path.join(OUTPUT_DIR, "preprocessor2.pkl"), compress=3)

# Transform the data and save processed copies for model training
X_train_processed = preprocessor.transform(X_train)
X_test_processed = preprocessor.transform(X_test)

np.save(os.path.join(OUTPUT_DIR, "X_train.npy"), X_train_processed)
np.save(os.path.join(OUTPUT_DIR, "X_test.npy"), X_test_processed)
np.save(os.path.join(OUTPUT_DIR, "y_train.npy"), y_train)
np.save(os.path.join(OUTPUT_DIR, "y_test.npy"), y_test)

print("\n✅ All preprocessing steps completed successfully.")
print(f"Files saved in: {OUTPUT_DIR}")
