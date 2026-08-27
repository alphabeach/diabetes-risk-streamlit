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

## Tech Stack

- **Frontend:** Streamlit
- **ML Model:** Gradient Boosting (AUC: 0.83)
- **AI Recommendations:** OpenRouter API (Claude 3.5 Sonnet)
- **Dataset:** BRFSS Diabetes Dataset (70,692 records, 21 features)

---

For full project documentation, training scripts, and model details, see the [root README](../README.md).
