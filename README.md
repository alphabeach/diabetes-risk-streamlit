# Diabetes Risk Streamlit

AI-powered pre-diabetes risk prediction tool built with Streamlit and scikit-learn.

## About

Assess your pre-diabetes risk based on lifestyle and health indicators. The app uses a Gradient Boosting model trained on the BRFSS dataset (70,000+ records) to provide instant risk predictions with personalized insights.

## Features

- **Instant Risk Assessment** — Get your diabetes risk score in seconds
- **Personalized Insights** — AI-generated health recommendations via OpenRouter API
- **Factor Analysis** — See which lifestyle factors affect your risk most
- **PDF Reports** — Download a summary of your assessment
- **Population Comparison** — Compare your results to national averages
- **Admin Dashboard** — View assessment history and statistics

## How It Works

1. Fill out the health assessment form with 21 lifestyle/health indicators
2. The Gradient Boosting model analyzes your inputs
3. Receive your risk score (Low / Moderate / High)
4. Get personalized AI-powered recommendations to reduce your risk

> **Note:** The app may take a minute or two to load on first visit if no users are currently active. This is normal — the server is warming up.

---

## Streamlit App

### Project Structure

```
health-risk-assessment/
├── app.py                 # Application entry point
├── config.py              # Configuration and feature definitions
├── src/
│   ├── components/        # UI components (forms, displays, charts)
│   ├── utils/             # Utilities (predictor, PDF, database, API)
│   ├── models/            # Risk model logic
│   └── data/              # Health tips and risk factor data
├── models/                # Trained model files (.pkl)
└── requirements.txt
```

### Running the App

```bash
git clone https://github.com/alphabeach/diabetes-risk-streamlit.git
cd diabetes-risk-streamlit
pip install -r health-risk-assessment/requirements.txt
cd health-risk-assessment
streamlit run app.py
```

---

## Training Pipeline

### Project Structure

```
scripts/
├── preprocessing.py       # Data loading and feature engineering
├── confusion.py           # Model training, evaluation, and confusion matrices
├── visualization.py       # ROC, calibration, and probability plots
├── metrics.py             # Model metrics and calibration analysis
└── predict.py             # CLI-based risk predictor
```

### Training Models

```bash
cd scripts
python preprocessing.py    # Preprocess data
python confusion.py        # Train models, evaluate, and generate confusion matrices
python visualization.py    # Generate ROC, calibration, and probability plots
python metrics.py          # Detailed model metrics and calibration analysis
```

### Models

| Model | AUC | F1 Score |
|-------|-----|----------|
| Gradient Boosting | 0.830 | 0.764 |
| Logistic Regression | 0.823 | 0.750 |
| Linear SVM | 0.823 | 0.750 |

---

## Tech Stack

- **Frontend:** Streamlit
- **ML:** scikit-learn, imbalanced-learn
- **AI Recommendations:** OpenRouter API (Claude 3.5 Sonnet)
- **PDF:** ReportLab
- **Dataset:** BRFSS Diabetes Dataset (70,692 records, 21 features)
