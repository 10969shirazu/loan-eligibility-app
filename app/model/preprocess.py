# preprocess.py
import pandas as pd

def preprocess_input(data: dict, label_encoders: dict) -> pd.DataFrame:
    """
    Transforme les données brutes d'un utilisateur en DataFrame prêt à être utilisé par le modèle.
    Utilise les vrais encodeurs sauvegardés lors de l'entraînement.
    """
    df = pd.DataFrame([{key: data.get(key) for key in data}])

    # Forcer types numériques sur certaines colonnes
    num_cols = ['loan_amnt', 'annual_inc', 'int_rate']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Encoder les colonnes catégoriques
    cat_cols = ['term', 'emp_length', 'home_ownership', 'verification_status']
    for col in cat_cols:
        if col in df.columns and col in label_encoders:
            df[col] = label_encoders[col].transform(df[col])
        else:
            df[col] = 0  # Default fallback si la valeur est inconnue

    # Ajouter les features manquantes avec des valeurs par défaut (0)
    expected_features = ['loan_amnt', 'term', 'int_rate', 'installment', 'grade', 'sub_grade',
                         'emp_length', 'home_ownership', 'annual_inc', 'verification_status',
                         'purpose', 'dti', 'delinq_2yrs', 'inq_last_6mths', 'open_acc',
                         'pub_rec', 'revol_bal', 'revol_util', 'total_acc', 'last_pymnt_amnt']

    for feature in expected_features:
        if feature not in df.columns:
            df[feature] = 0

    df = df[expected_features]  # Assurer l'ordre des colonnes

    return df
