# Hospital Readmission Predictor

An end-to-end data science project that predicts 30-day hospital 
readmission risk using real clinical data.

## Problem Statement
Hospitals lose millions in CMS penalties when patients are readmitted 
within 30 days of discharge. This project builds an ML pipeline that 
flags high-risk patients before discharge so clinicians can intervene.

## Tech Stack
- **SQL** — PostgreSQL database with 101,766 patient records
- **Python** — EDA, feature engineering, ML model training
- **XGBoost** — Champion ML model with SHAP explainability  
- **Tableau** — Interactive 4-panel risk dashboard
- **Flask** — REST API serving live risk predictions

## Dataset
Diabetes 130-US Hospitals (1999-2008) — UCI ML Repository  
101,766 encounters · 50 features · 11.2% readmission rate

## Results
| Model | ROC-AUC |
|---|---|
| Logistic Regression | 0.54 |
| Random Forest | 0.55 |
| XGBoost | Best |

## Project Structure
hospital_readmission/
├── data/
│   ├── raw/               # Original CSV
│   └── processed/         # Feature engineered CSVs
├── sql/                   # Schema + queries
├── src/                   # Python scripts
├── api/                   # Flask REST API
├── models/                # Saved ML models
├── tableau/               # Dashboard + data
└── notebooks/             # EDA + training notebooks

## How to Run

### 1. Setup
pip install -r requirements.txt

### 2. Load data into PostgreSQL
python3 src/load_data.py

### 3. Start the API
python3 api/app.py

### 4. Test prediction
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"age_num": 75, "is_male": 1, "time_in_hospital": 7,
       "number_inpatient": 3, "on_insulin": 1}'

## API Response Example
{
  "risk_score": 0.685,
  "risk_level": "HIGH", 
  "prediction": 1,
  "message": "Patient has HIGH readmission risk"
}

## Key Findings
- Patients aged 80-90 have highest readmission rates (12%)
- Prior inpatient visits are the strongest readmission predictor
- 37,039 patients classified as HIGH risk (36% of total)
- Insulin-dependent patients have 2x higher readmission risk