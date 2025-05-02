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
