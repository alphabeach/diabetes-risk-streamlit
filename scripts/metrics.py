import os
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import (
    brier_score_loss,
    roc_auc_score,
    average_precision_score,
    precision_recall_curve,
    auc
)
from sklearn.calibration import calibration_curve

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

MODEL_PATH = os.path.join(ROOT_DIR, "models", "Gradient_Boosting.pkl")
PREPROCESSOR_PATH = os.path.join(ROOT_DIR, "models", "preprocessor2.pkl")
DATA_PATH = os.path.join(ROOT_DIR, "data", "diabetes2.csv")
SAVE_PLOT_PATH = os.path.join(ROOT_DIR, "outputs", "plots", "calibration_curve.png")
Q_BINS = 3
LABELS = ["Low", "Moderate", "High"]

print("🔄 Loading model and preprocessor…")
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)
print("✅ Loaded model & preprocessor.")


df = pd.read_csv(DATA_PATH)
X = df.drop(columns=["Diabetes_binary"]) 
y = df["Diabetes_binary"]

X_proc = preprocessor.transform(X)
y_true = y.values.ravel()
y_prob = model.predict_proba(X_proc)[:, 1]

roc_auc = roc_auc_score(y_true, y_prob)
avg_precision = average_precision_score(y_true, y_prob)
precision_vals, recall_vals, pr_thresholds = precision_recall_curve(y_true, y_prob)
pr_auc = auc(recall_vals, precision_vals)
brier = brier_score_loss(y_true, y_prob)

print(f"ROC AUC: {roc_auc:.4f}")
print(f"Average Precision (PR AUC): {avg_precision:.4f}")
print(f"PR AUC (via auc): {pr_auc:.4f}")
print(f"Brier Score: {brier:.6f}")

try:
    bins = pd.qcut(y_prob, q=Q_BINS, labels=LABELS, retbins=False, duplicates="raise")
    bins_edges = pd.qcut(y_prob, q=Q_BINS, retbins=True, duplicates="raise")[1]
except Exception:
    edges = np.quantile(y_prob, np.linspace(0,1,Q_BINS+1))
    if np.unique(edges).size < edges.size:
        edges = np.linspace(np.min(y_prob), np.max(y_prob), Q_BINS+1)
    bins_edges = edges
    bins = pd.cut(y_prob, bins=bins_edges, labels=LABELS[:len(bins_edges)-1],
                  include_lowest=True, right=True)

df_bins = pd.DataFrame({"prob": y_prob, "actual": y_true, "bin": bins})
calibration_table = df_bins.groupby("bin").agg(
    predicted_mean=("prob", "mean"),
    observed_rate=("actual", "mean"),
    count=("actual", "count")
).reset_index()

print("\n=== Calibration Table ===")
print(calibration_table.to_string(index=False))

for i in range(len(bins_edges)-1):
    left = bins_edges[i]
    right = bins_edges[i+1]
    lab = LABELS[i] if i < len(LABELS) else f"Bin{i+1}"
    print(f"{lab}: {left:.4f} – {right:.4f}")

# Suggest threshold
observed = calibration_table["observed_rate"].values
suggested_threshold = None
if observed.size >= 2:
    diffs = np.diff(observed)
    split_index = int(np.argmax(np.abs(diffs)))
    suggested_threshold = float(bins_edges[split_index+1])
    print(f"Suggested threshold between '{LABELS[split_index]}' and '{LABELS[split_index+1]}': {suggested_threshold:.4f}")

prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10, strategy='quantile')
plt.figure(figsize=(8,6))
plt.plot(prob_pred, prob_true, marker='o', linestyle='-', label='Calibration curve')
plt.plot([0,1],[0,1], linestyle='--', label='Perfectly calibrated')
plt.xlabel('Mean predicted probability')
plt.ylabel('Observed fraction of positives')
plt.title('Calibration curve')
plt.legend()
plt.grid(True)
plt.savefig(SAVE_PLOT_PATH, dpi=300, bbox_inches='tight')
print(f"Plot saved to: {SAVE_PLOT_PATH}")
plt.show()
