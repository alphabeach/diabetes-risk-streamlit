# Diabetes Risk Streamlit

An AI-powered web application for predicting pre-diabetes risk based on lifestyle indicators. Built with Streamlit and machine learning models trained on the BRFSS (Behavioral Risk Factor Surveillance System) dataset.

## Features

- **Risk Prediction** — Real-time diabetes risk assessment using Gradient Boosting, Logistic Regression, and Linear SVM models
- **Personalized Insights** — AI-generated health recommendations via OpenRouter API
- **Factor Analysis** — Breakdown of individual risk contributors with visual comparisons
- **PDF Reports** — Downloadable summary of assessment results
- **Admin Dashboard** — View assessment history and population statistics

## Project Structure

```
.
├── health-risk-assessment/    # Streamlit web application
│   ├── app.py                 # Application entry point
│   ├── config.py              # Configuration and feature definitions
│   ├── src/
│   │   ├── components/        # UI components (forms, displays, charts)
│   │   ├── utils/             # Utilities (predictor, PDF, database, API)
│   │   ├── models/            # Risk model logic
│   │   └── data/              # Health tips and risk factor data
│   ├── models/                # Trained model files (.pkl)
│   └── requirements.txt
├── scripts/                   # ML training and evaluation pipeline
│   ├── preprocessing.py       # Data loading and feature engineering
│   ├── confusion.py           # Model training, evaluation, and confusion matrices
│   ├── visualization.py       # ROC, calibration, and probability plots
│   ├── metrics.py             # Model metrics and calibration analysis
│   └── predict.py             # CLI-based risk predictor
├── data/                      # Training datasets
├── models/                    # Saved models and preprocessors
└── outputs/                   # Evaluation results and plots
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/alphabeach/diabetes-risk-streamlit.git
cd diabetes-risk-streamlit
pip install -r health-risk-assessment/requirements.txt
```

### Running the App

```bash
cd health-risk-assessment
streamlit run app.py
```

### Training Models

```bash
cd scripts
python preprocessing.py    # Preprocess data
python confusion.py        # Train models, evaluate, and generate confusion matrices
python visualization.py    # Generate ROC, calibration, and probability plots
python metrics.py          # Detailed model metrics and calibration analysis
```

## Models

| Model | AUC | F1 Score |
|-------|-----|----------|
| Gradient Boosting | 0.830 | 0.764 |
| Logistic Regression | 0.823 | 0.750 |
| Linear SVM | 0.823 | 0.750 |

## Tech Stack

- **Frontend:** Streamlit
- **ML:** scikit-learn, imbalanced-learn
- **API:** OpenRouter (Claude 3.5 Sonnet)
- **PDF:** ReportLab
- **Data:** BRFSS Diabetes Dataset
