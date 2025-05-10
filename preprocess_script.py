# preprocessing_script.py

import pandas as pd

# Fonction de prétraitement sans label_encoders
def preprocess_input(test_data: pd.DataFrame) -> pd.DataFrame:
    # Mappings manuels
    term_map = {" 36 months": 0, " 60 months": 1}
    emp_length_map = {
        '< 1 year': 0, '1 year': 1, '2 years': 2, '3 years': 3, '4 years': 4,
        '5 years': 5, '6 years': 6, '7 years': 7, '8 years': 8, '9 years': 9,
        '10+ years': 10
    }
    home_ownership_map = {'RENT': 0, 'MORTGAGE': 1, 'OWN': 2, 'OTHER': 3}
    verification_map = {'Not Verified': 0, 'Source Verified': 1, 'Verified': 2}
    purpose_map = {'credit_card': 0, 'debt_consolidation': 1, 'small_business': 2}

    df = test_data.copy()

    # Appliquer les mappings
    df['term'] = df['term'].map(term_map).fillna(0)
    df['emp_length'] = df['emp_length'].map(emp_length_map).fillna(0)
    df['home_ownership'] = df['home_ownership'].map(home_ownership_map).fillna(0)
    df['verification_status'] = df['verification_status'].map(verification_map).fillna(0)
    df['purpose'] = df['purpose'].map(purpose_map).fillna(0)

    # Ajouter les colonnes manquantes avec 0
    expected_features = [
        'loan_amnt', 'term', 'int_rate', 'installment', 'grade', 'sub_grade',
        'emp_length', 'home_ownership', 'annual_inc', 'verification_status',
        'purpose', 'dti', 'delinq_2yrs', 'inq_last_6mths', 'open_acc',
        'pub_rec', 'revol_bal', 'revol_util', 'total_acc', 'last_pymnt_amnt'
    ]

    for feature in expected_features:
        if feature not in df.columns:
            df[feature] = 0

    df = df[expected_features]

    return df
