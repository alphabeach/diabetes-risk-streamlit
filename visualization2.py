# visualization_probability.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.calibration import calibration_curve

# === Paths ===
OUTPUT_DIR = "outputs"
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# === Identify model probability files ===
prob_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith("_probabilities.csv")]

if not prob_files:
    print("⚠️ No probability files found in outputs/. Please run analysis first.")
    exit()

# === Load probability data for all models ===
model_data = {}
for file in prob_files:
    model_name = file.replace("_probabilities.csv", "")
    df = pd.read_csv(os.path.join(OUTPUT_DIR, file))
    model_data[model_name] = df
    print(f"✅ Loaded {file} ({df.shape[0]} rows)")

# === ROC Curve ===
plt.figure(figsize=(8, 6))
for model_name, df in model_data.items():
    fpr, tpr, _ = roc_curve(df["Actual"], df["Predicted_Prob"])
    auc = roc_auc_score(df["Actual"], df["Predicted_Prob"])
    plt.plot(fpr, tpr, label=f"{model_name} (AUC = {auc:.3f})")

plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.title("ROC Curve - Model Comparison")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "roc_curve_comparison.png"))
print("✅ ROC curve saved.")
plt.show()

# === Calibration Curve ===
plt.figure(figsize=(8, 6))
for model_name, df in model_data.items():
    prob_true, prob_pred = calibration_curve(df["Actual"], df["Predicted_Prob"], n_bins=10)
    plt.plot(prob_pred, prob_true, marker="o", label=model_name)

plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.title("Calibration Curve - Model Comparison")
plt.xlabel("Predicted Probability")
plt.ylabel("True Probability")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "calibration_curve_comparison.png"))
print("✅ Calibration curve saved.")
plt.show()

# === Probability Distribution Plot ===
for model_name, df in model_data.items():
    plt.figure(figsize=(8, 6))
    plt.hist(
        df.loc[df["Actual"] == 0, "Predicted_Prob"],
        bins=30, alpha=0.6, label="Non-Diabetic", density=True
    )
    plt.hist(
        df.loc[df["Actual"] == 1, "Predicted_Prob"],
        bins=30, alpha=0.6, label="Diabetic", density=True
    )
    plt.title(f"Probability Distribution - {model_name}")
    plt.xlabel("Predicted Probability")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, f"{model_name}_probability_distribution.png"))
    plt.show()
    print(f"✅ Probability distribution saved for {model_name}")

print("\n✅ All visualizations completed and saved in:", PLOTS_DIR)
