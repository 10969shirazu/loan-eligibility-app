# test_m_final_safe.py

import pandas as pd
import joblib

# Charger le modèle, le scaler et les label encoders
model = joblib.load('app/models/loan_model_balanced.pkl')
scaler = joblib.load('app/models/scaler.pkl')
label_encoders = joblib.load('app/models/label_encoders.pkl')

# Créer plusieurs profils de test
test_profiles = pd.DataFrame([
    {
        'loan_amnt': 12000,
        'term': ' 36 months',
        'int_rate': 12.5,
        'installment': 0,
        'grade': 'B',
        'sub_grade': 'B2',
        'emp_length': '5 years',
        'home_ownership': 'MORTGAGE',
        'annual_inc': 55000,
        'verification_status': 'Source Verified',
        'purpose': 'credit_card',
        'dti': 18.5,
        'delinq_2yrs': 0,
        'inq_last_6mths': 2,
        'open_acc': 8,
        'pub_rec': 0,
        'revol_bal': 4000,
        'revol_util': 32.0,
        'total_acc': 22,
        'last_pymnt_amnt': 200
    },
    {
        'loan_amnt': 8000,
        'term': ' 60 months',
        'int_rate': 15.2,
        'installment': 0,
        'grade': 'C',
        'sub_grade': 'C4',
        'emp_length': '2 years',
        'home_ownership': 'RENT',
        'annual_inc': 30000,
        'verification_status': 'Not Verified',
        'purpose': 'small_business',
        'dti': 25.0,
        'delinq_2yrs': 1,
        'inq_last_6mths': 4,
        'open_acc': 5,
        'pub_rec': 0,
        'revol_bal': 5000,
        'revol_util': 65.0,
        'total_acc': 16,
        'last_pymnt_amnt': 120
    }
])

# Mapping manuel pour 'term'
term_map = {' 36 months': 36, ' 60 months': 60}
test_profiles['term'] = test_profiles['term'].map(term_map)

# Appliquer les LabelEncoders sauvegardés proprement
for col in ['grade', 'sub_grade', 'emp_length']:
    if col in test_profiles.columns and col in label_encoders:
        encoder = label_encoders[col]
        classes = encoder.classes_
        test_profiles[col] = test_profiles[col].apply(lambda x: x if x in classes else classes[0])
        test_profiles[col] = encoder.transform(test_profiles[col].astype(str))

# One-hot encoding pour les colonnes catégoriques
test_profiles = pd.get_dummies(test_profiles, columns=['home_ownership', 'verification_status', 'purpose'], drop_first=True)

# S'assurer que toutes les colonnes attendues sont là
expected_features = scaler.feature_names_in_

for feature in expected_features:
    if feature not in test_profiles.columns:
        test_profiles[feature] = 0

# Réordonner les colonnes
test_profiles = test_profiles[expected_features]

# Normaliser
input_scaled = scaler.transform(test_profiles)

# Prédire
predictions = model.predict(input_scaled)

# Résultats
test_profiles['eligibility_prediction'] = ['Eligible' if pred == 1 else 'Not Eligible' for pred in predictions]

# Afficher
print(test_profiles[['loan_amnt', 'annual_inc', 'eligibility_prediction']])

for index, row in test_profiles.iterrows():
    print(f"Loan Amount: {row['loan_amnt']}, Annual Income: {row['annual_inc']}, Eligibility: {row['eligibility_prediction']}")
