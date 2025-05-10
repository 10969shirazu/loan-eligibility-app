# predictor.py
import joblib
import os
import pandas as pd


BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Récupère le dossier où est predictor.py
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'loan_model_balanced.pkl')
ENCODERS_PATH = os.path.join(BASE_DIR, '..', 'models', 'label_encoders.pkl')


model = joblib.load(MODEL_PATH)
label_encoders = joblib.load(ENCODERS_PATH)

def predict_eligibility(processed_input):
    """
    Prend en entrée un DataFrame (1 ligne), retourne True (éligible) ou False (non éligible).
    """
    if not isinstance(processed_input, pd.DataFrame):
        raise ValueError("Entrée attendue : DataFrame pandas (1 ligne).")

    prediction = model.predict(processed_input)
    return bool(prediction[0])
def get_refusal_reason(input_df):
    row = input_df.iloc[0]

    try:
        if float(row['dti']) > 35:
            return "Your debt-to-income ratio exceeds 35%."
        if float(row['annual_inc']) < 20000:
            return "Your annual income is below the minimum threshold."
        if int(row['delinq_2yrs']) > 0:
            return "Your credit history shows recent delinquencies."
        if int(row['inq_last_6mths']) > 5:
            return "You have too many recent credit inquiries."
        if float(row['revol_util']) > 80:
            return "Your credit utilization is too high."
    except Exception as e:
        return f"Refusal explanation error: {str(e)}"

    return "Your profile does not meet the current eligibility criteria."
