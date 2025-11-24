# analysis_probability.py

import numpy as np
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
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

# === Paths ===
MODEL_DIR = "models"
OUTPUT_DIR = "outputs"
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

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

    # === Save confusion matrix as image ===
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Predicted: Non-Diabetic", "Predicted: Diabetic"],
        yticklabels=["Actual: Non-Diabetic", "Actual: Diabetic"]
    )
    plt.title(f"Confusion Matrix - {name}")
    plt.ylabel("Actual Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    cm_path = os.path.join(PLOTS_DIR, f"{name}_confusion_matrix.png")
    plt.savefig(cm_path)
    plt.close()
    print(f"🖼️ Confusion matrix image saved: {cm_path}")

    # === Save model + predictions ===
    joblib.dump(model, os.path.join(MODEL_DIR, f"{name}.pkl"))
    pd.DataFrame({
        "Actual": y_test,
        "Predicted_Prob": y_pred_prob
    }).to_csv(os.path.join(OUTPUT_DIR, f"{name}_probabilities.csv"), index=False)

    # Collect metrics
    results.append({
        "Model": name,
        "AUC": auc,
        "BrierScore": brier,
        "Recall": recall,
        "Precision": precision,
        "F1_Score": f1,
        "TP": cm[1, 1],
        "TN": cm[0, 0],
        "FP": cm[0, 1],
        "FN": cm[1, 0]
    })

    print(f"✅ {name} completed. AUC={auc:.4f}, Recall={recall:.4f}, F1={f1:.4f}")

# === Save summary results ===
results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(OUTPUT_DIR, "model_evaluation_results.csv"), index=False)

print("\n✅ All models trained, evaluated, and confusion matrix images saved.")
print(results_df)
