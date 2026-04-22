from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load model and scaler
model = joblib.load('models/xgb_readmission_model.pkl')

print("Model loaded successfully!")

# Feature names must match training data
FEATURES = [
    'age_num', 'is_male', 'time_in_hospital',
    'num_lab_procedures', 'num_procedures', 'num_medications',
    'number_outpatient', 'number_emergency', 'number_inpatient',
    'number_diagnoses', 'a1c_high', 'on_insulin', 'med_changed',
    'on_diabetes_med', 'total_prior_visits', 'high_utilizer'
]

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Hospital Readmission Prediction API',
        'version': '1.0',
        'endpoints': {
            'POST /predict': 'Get readmission risk score for a patient',
            'GET /health': 'Check API health'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model': 'XGBoost'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Build feature dataframe
        patient = {
            'age_num'           : data.get('age_num', 65),
            'is_male'           : data.get('is_male', 0),
            'time_in_hospital'  : data.get('time_in_hospital', 4),
            'num_lab_procedures': data.get('num_lab_procedures', 43),
            'num_procedures'    : data.get('num_procedures', 1),
            'num_medications'   : data.get('num_medications', 16),
            'number_outpatient' : data.get('number_outpatient', 0),
            'number_emergency'  : data.get('number_emergency', 0),
            'number_inpatient'  : data.get('number_inpatient', 0),
            'number_diagnoses'  : data.get('number_diagnoses', 7),
            'a1c_high'          : data.get('a1c_high', 0),
            'on_insulin'        : data.get('on_insulin', 0),
            'med_changed'       : data.get('med_changed', 0),
            'on_diabetes_med'   : data.get('on_diabetes_med', 1),
            'total_prior_visits': data.get('total_prior_visits', 0),
            'high_utilizer'     : data.get('high_utilizer', 0)
        }

        df = pd.DataFrame([patient])
        risk_score = model.predict_proba(df)[0][1]
        prediction = model.predict(df)[0]

        # Risk level
        if risk_score >= 0.5:
            risk_level = 'HIGH'
        elif risk_score >= 0.3:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'

        return jsonify({
            'risk_score'  : round(float(risk_score), 3),
            'risk_level'  : risk_level,
            'prediction'  : int(prediction),
            'message'     : f'Patient has {risk_level} readmission risk',
            'patient_data': patient
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    try:
        data = request.get_json()
        patients = data.get('patients', [])
        if not patients:
            return jsonify({'error': 'No patients provided'}), 400

        df = pd.DataFrame(patients)[FEATURES]
        scores = model.predict_proba(df)[:, 1]
        preds  = model.predict(df)

        results = []
        for i, (score, pred) in enumerate(zip(scores, preds)):
            if score >= 0.5:
                level = 'HIGH'
            elif score >= 0.3:
                level = 'MEDIUM'
            else:
                level = 'LOW'
            results.append({
                'patient_index': i,
                'risk_score'   : round(float(score), 3),
                'risk_level'   : level,
                'prediction'   : int(pred)
            })

        return jsonify({
            'total_patients': len(results),
            'high_risk'     : sum(1 for r in results if r['risk_level'] == 'HIGH'),
            'medium_risk'   : sum(1 for r in results if r['risk_level'] == 'MEDIUM'),
            'low_risk'      : sum(1 for r in results if r['risk_level'] == 'LOW'),
            'results'       : results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)