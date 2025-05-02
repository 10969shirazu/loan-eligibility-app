# routes.py
from flask import Blueprint, render_template, request, render_template, redirect, url_for, flash
from app.model.preprocess import preprocess_input
from app.model.predictor import predict_eligibility, label_encoders
from flask import request, render_template
import pandas as pd
import joblib
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Récupère le dossier où est predictor.py
MODEL_PATH = os.path.join(BASE_DIR,  'models', 'loan_model_balanced.pkl')
ENCODERS_PATH = os.path.join(BASE_DIR,  'models', 'label_encoders.pkl')
SCALER_PATH = os.path.join(BASE_DIR,  'models', 'scaler.pkl')

# Charger modèle, scaler, label_encoders une seule fois au démarrage
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
label_encoders = joblib.load(ENCODERS_PATH)

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@main.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer les données du formulaire
        form_data = request.form.to_dict()

        # Préparer le DataFrame d'un seul utilisateur
        input_data = pd.DataFrame([form_data])

        # Convertir correctement les colonnes
        input_data['term'] = input_data['term'].map({' 36 months': 36, ' 60 months': 60})

        for col in ['grade', 'sub_grade', 'emp_length']:
            if col in input_data.columns and col in label_encoders:
                encoder = label_encoders[col]
                classes = encoder.classes_
                input_data[col] = input_data[col].apply(lambda x: x if x in classes else classes[0])
                input_data[col] = encoder.transform(input_data[col].astype(str))

        # One-hot encoding
        input_data = pd.get_dummies(input_data, columns=['home_ownership', 'verification_status', 'purpose'], drop_first=True)

        # Remplir colonnes manquantes
        expected_features = scaler.feature_names_in_
        for feature in expected_features:
            if feature not in input_data.columns:
                input_data[feature] = 0

        # Réordonner les colonnes
        input_data = input_data[expected_features]

        # Normaliser
        input_scaled = scaler.transform(input_data)

        # Prédire
        prediction = model.predict(input_scaled)
        eligible = bool(prediction[0])

        # Retourner vers result.html avec le résultat
        return render_template('result.html', eligible=eligible)
    except Exception as e:
        # Capture toute erreur inattendue
        print(f"Erreur interne: {str(e)}")
        flash("An internal error occurred. Please try again.", 'error')
        return redirect(url_for('main.index'))
