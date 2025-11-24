import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
import os

FILE_PATH = "data/diabetes.csv"
MODEL_DIR = "models"

def preprocess_data():
    df = pd.read_csv(FILE_PATH)
    df = df.drop_duplicates().dropna()

    categorical_cols = [
        'HighBP', 'HighChol', 'CholCheck', 'Smoker', 'Stroke',
        'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
        'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost',
        'DiffWalk', 'Sex', 'Age', 'Education', 'Income'
    ]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')

    df['Diabetes_binary'] = df['Diabetes_012'].apply(lambda x: 1 if x == 2 else 0)
    X = df.drop(['Diabetes_012', 'Diabetes_binary'], axis=1)
    y = df['Diabetes_binary']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    sm = SMOTE(random_state=42)
    X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

    numeric_features = ['BMI', 'GenHlth', 'MentHlth', 'PhysHlth']
    categorical_features = [col for col in X.columns if col not in numeric_features]

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_features)
    ])

    X_train_ready = preprocessor.fit_transform(X_train_res)
    X_test_ready = preprocessor.transform(X_test)

    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    joblib.dump(preprocessor, os.path.join(MODEL_DIR, "preprocessor.pkl"))

    print("✅ Preprocessing complete!")
    print("X_train shape:", X_train_ready.shape)
    print("X_test shape:", X_test_ready.shape)
    print("y_train shape:", y_train_res.shape)
    print("y_test shape:", y_test.shape)
    print("💾 Preprocessor saved to models/preprocessor.pkl")

    return X_train_ready, X_test_ready, y_train_res, y_test, preprocessor


if __name__ == "__main__":
    preprocess_data()
