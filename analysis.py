import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, classification_report
from preprocessing import preprocess_data

MODEL_DIR = "models"
RESULTS_FILE = os.path.join(MODEL_DIR, "analysis_results.csv")

def train_and_save_models():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    print("🔄 Loading and preprocessing data...")
    X_train, X_test, y_train, y_test, preprocessor = preprocess_data()

    models = {
        "Logistic_Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Linear_SVM": LinearSVC(max_iter=2000, random_state=42),
        "Gradient_Boosting": LGBMClassifier(n_estimators=200, max_depth=12, n_jobs=-1, random_state=42)
    }

    results_summary = []

    for name, model in models.items():
        print(f"\n🚀 Training {name.replace('_', ' ')}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, digits=4, output_dict=True)
        print(f"{name.replace('_', ' ')} Accuracy: {acc:.4f}")

        # Append summary for saving
        results_summary.append({
            "Model": name,
            "Accuracy": acc,
            "Precision_0": report['0']['precision'],
            "Recall_0": report['0']['recall'],
            "F1_0": report['0']['f1-score'],
            "Precision_1": report['1']['precision'],
            "Recall_1": report['1']['recall'],
            "F1_1": report['1']['f1-score']
        })

        # Save trained model
        joblib.dump(model, os.path.join(MODEL_DIR, f"{name}.pkl"))
        print(f"💾 {name} saved to {MODEL_DIR}/{name}.pkl")

    # Save preprocessor
    joblib.dump(preprocessor, os.path.join(MODEL_DIR, "preprocessor.pkl"))
    print(f"💾 Preprocessor saved to {MODEL_DIR}/preprocessor.pkl")

    # Save analysis results to CSV
    df_results = pd.DataFrame(results_summary)
    df_results.to_csv(RESULTS_FILE, index=False)
    print(f"💾 Analysis results saved to {RESULTS_FILE}")

    # Print summary
    print("\n✅ Summary of Model Performance:")
    print(df_results)


if __name__ == "__main__":
    train_and_save_models()
