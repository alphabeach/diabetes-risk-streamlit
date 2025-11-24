import numpy as np
import pandas as pd
import os
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    roc_auc_score,
    brier_score_loss,
    recall_score,
    precision_score,
    f1_score,
    confusion_matrix
)
import joblib

# === Load preprocessed data ===
MODEL_DIR = "models"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading preprocessed data...")
X_train = np.load(os.path.join(MODEL_DIR, "X_train.npy"))
X_test = np.load(os.path.join(MODEL_DIR, "X_test.npy"))
y_train = np.load(os.path.join(MODEL_DIR, "y_train.npy"))
y_test = np.load(os.path.join(MODEL_DIR, "y_test.npy"))
print(f"✅ Data loaded: Train={X_train.shape}, Test={X_test.shape}")

# === Initialize models ===
models = {
    "Logistic_Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Linear_SVM": CalibratedClassifierCV(LinearSVC(random_state=42, max_iter=10000)),
    "Gradient_Boosting": GradientBoostingClassifier(random_state=42)
}

results = []

# === Train and evaluate models ===
for name, model in models.items():
    print(f"\n🚀 Training {name}...")
    model.fit(X_train, y_train)
    print("✅ Training complete.")

    # Predict probabilities and labels
    y_pred_prob = model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_prob >= 0.5).astype(int)

    # Evaluate performance
    auc = roc_auc_score(y_test, y_pred_prob)
    brier = brier_score_loss(y_test, y_pred_prob)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    results.append({
        "Model": name,
        "AUC": auc,
        "BrierScore": brier,
        "Recall": recall,
        "Precision": precision,
        "F1_Score": f1
    })

    # Save trained model
    joblib.dump(model, os.path.join(MODEL_DIR, f"{name}.pkl"))

    # Save prediction probabilities for visualization
    pd.DataFrame({
        "Actual": y_test,
        "Predicted_Prob": y_pred_prob
    }).to_csv(os.path.join(OUTPUT_DIR, f"{name}_probabilities.csv"), index=False)

    print(f"✅ {name} completed. AUC={auc:.4f}, Recall={recall:.4f}, F1={f1:.4f}")

# === Save all results ===
results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(OUTPUT_DIR, "model_evaluation_results.csv"), index=False)
print("\n✅ All models trained and evaluated successfully.")
print(results_df)
