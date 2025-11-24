import os
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc, precision_recall_curve
import pandas as pd

MODEL_DIR = "models"
RESULTS_FILE = os.path.join(MODEL_DIR, "analysis_results.csv")

def visualize_models():
    # Load preprocessed data
    preprocessor = joblib.load(os.path.join(MODEL_DIR, "preprocessor.pkl"))
    df_results = pd.read_csv(RESULTS_FILE)

    # Load original dataset and preprocess (only scaling/encoding)
    from preprocessing import FILE_PATH
    df = pd.read_csv(FILE_PATH).drop_duplicates().dropna()
    df['Diabetes_binary'] = df['Diabetes_012'].apply(lambda x: 1 if x == 2 else 0)
    X = df.drop(['Diabetes_012', 'Diabetes_binary'], axis=1)
    y = df['Diabetes_binary']

    # Split (same as before, 20% test)
    from sklearn.model_selection import train_test_split
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    X_test_ready = preprocessor.transform(X_test)

    # Load models
    model_files = [f for f in os.listdir(MODEL_DIR) if f.endswith(".pkl") and f != "preprocessor.pkl"]
    models = {f.replace(".pkl", ""): joblib.load(os.path.join(MODEL_DIR, f)) for f in model_files}

    # --- 1️⃣ Confusion Matrix ---
    for name, model in models.items():
        y_pred = model.predict(X_test_ready)
        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap='Blues')
        plt.title(f"{name} - Confusion Matrix")
        plt.savefig(os.path.join(MODEL_DIR, f"{name}_confusion_matrix.png"), bbox_inches='tight')
        plt.show()

    # --- 2️⃣ ROC Curve ---
    plt.figure()
    for name, model in models.items():
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test_ready)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, lw=2, label=f"{name} (AUC = {roc_auc:.3f})")

    plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve Comparison")
    plt.legend(loc="lower right")
    plt.savefig(os.path.join(MODEL_DIR, "roc_curve_comparison.png"), bbox_inches='tight')
    plt.show()

    # --- 3️⃣ Precision-Recall Curve ---
    plt.figure()
    for name, model in models.items():
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test_ready)[:, 1]
            precision, recall, _ = precision_recall_curve(y_test, y_prob)
            plt.plot(recall, precision, lw=2, label=name)

    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve Comparison")
    plt.legend(loc="lower left")
    plt.savefig(os.path.join(MODEL_DIR, "precision_recall_comparison.png"), bbox_inches='tight')
    plt.show()

    # --- 4️⃣ Feature Importance (Gradient Boosting only) ---
    if "Gradient_Boosting" in models:
        gbm = models["Gradient_Boosting"]
        try:
            ohe = preprocessor.named_transformers_['cat']
            cat_features = ohe.get_feature_names_out(preprocessor.transformers_[1][2])
            feature_names = np.concatenate([preprocessor.transformers_[0][2], cat_features])
        except Exception:
            feature_names = np.arange(X_test_ready.shape[1])

        importances = gbm.feature_importances_
        indices = np.argsort(importances)[-10:][::-1]

        plt.figure(figsize=(8, 6))
        plt.barh(range(len(indices)), importances[indices][::-1])
        plt.yticks(range(len(indices)), feature_names[indices][::-1])
        plt.xlabel("Importance")
        plt.title("Top 10 Important Features (Gradient Boosting)")
        plt.tight_layout()
        plt.savefig(os.path.join(MODEL_DIR, "Gradient_Boosting_feature_importance.png"), bbox_inches='tight')
        plt.show()

    print("✅ Visualization complete! Plots saved in models/ folder.")


if __name__ == "__main__":
    visualize_models()
