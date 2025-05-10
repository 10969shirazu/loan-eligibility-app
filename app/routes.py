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
        # import
        from app import db
        from app.models import LoanRequest
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
        
        # Extraire la raison du refus si inéligible
        from app.model.predictor import get_refusal_reason
        reason = None
        if not eligible:
            reason = get_refusal_reason(input_data)

        # Sauvegarder la demande en base
        loan = LoanRequest(
            name=form_data.get('name'),
            phone=form_data.get('phone'),
            loan_amnt=float(form_data.get('loan_amnt')),
            term=input_data['term'].iloc[0],
            annual_inc=float(form_data.get('annual_inc')),
            int_rate=float(form_data.get('int_rate')),
            emp_length=form_data.get('emp_length'),
            home_ownership=form_data.get('home_ownership'),
            verification_status=form_data.get('verification_status'),
            purpose=form_data.get('purpose'),
            dti=float(form_data.get('dti')),
            delinq_2yrs=int(form_data.get('delinq_2yrs')),
            inq_last_6mths=int(form_data.get('inq_last_6mths')),
            open_acc=int(form_data.get('open_acc')),
            pub_rec=int(form_data.get('pub_rec')),
            revol_bal=float(form_data.get('revol_bal')),
            revol_util=float(form_data.get('revol_util')),
            total_acc=int(form_data.get('total_acc')),
            last_pymnt_amnt=float(form_data.get('last_pymnt_amnt')),
            result='Eligible' if eligible else 'Not Eligible',
            reason=reason
        )

        db.session.add(loan)
        db.session.commit()
        

        print(f"Loan request saved: {loan}")

        # Retourner vers result.html avec le résultat
        return render_template('result.html', eligible=eligible, reason=reason)
    except Exception as e:
        # Capture toute erreur inattendue
        print(f"Erreur interne: {str(e)}")
        flash("An internal error occurred. Please try again.", 'error')
        return redirect(url_for('main.home'))

@main.route('/admin/requests')
def admin_requests():
    all_requests = LoanRequest.query.order_by(LoanRequest.created_at.desc()).all()
    return render_template('admin_requests.html', requests=all_requests)

from flask import send_file
from io import BytesIO
import pandas as pd
from app.models import LoanRequest

@main.route('/admin/export')
def export_excel():
    loans = LoanRequest.query.order_by(LoanRequest.created_at.desc()).all()

    data = [{
        'Name': loan.name,
        'Phone': loan.phone,
        'Loan Amount': loan.loan_amnt,
        'Term': int.from_bytes(loan.term, byteorder='little' if isinstance(loan.term, bytes) else loan.term),
        'Income': loan.annual_inc,
        'Result': loan.result,
        'Created At': loan.created_at.strftime('%Y-%m-%d %H:%M')
    } for loan in loans]

    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Loan Requests')

    output.seek(0)

    return send_file(output,
                     as_attachment=True,
                     download_name='loan_requests.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# from flask import make_response, render_template
# from weasyprint import HTML
# from io import BytesIO

# @main.route('/admin/export/pdf')
# def export_pdf():
#     loans = LoanRequest.query.order_by(LoanRequest.created_at.desc()).all()

#     rendered = render_template('admin_export.html', requests=loans)
#     pdf_io = BytesIO()
#     HTML(string=rendered).write_pdf(pdf_io)
#     pdf_io.seek(0)

#     return send_file(pdf_io,
#                      as_attachment=True,
#                      download_name='loan_requests.pdf',
#                      mimetype='application/pdf')

def get_refusal_reason(data):
    reasons = []

    try:
        dti = float(data['dti'].iloc[0])
        income = float(data['annual_inc'].iloc[0])
        inquiries = int(data['inq_last_6mths'].iloc[0])
        delinq = int(data['delinq_2yrs'].iloc[0])
        revol_util = float(data['revol_util'].iloc[0])
    except Exception:
        return "insufficient or invalid data"

    if dti > 35:
        reasons.append("high debt-to-income ratio (DTI > 35%)")
    if income < 20000:
        reasons.append("low annual income (< 20k)")
    if inquiries > 5:
        reasons.append("too many recent credit inquiries")
    if delinq > 1:
        reasons.append("multiple past delinquencies")
    if revol_util > 80:
        reasons.append("revolving credit utilization is too high (> 80%)")

    return reasons[0] if reasons else "general eligibility criteria not met"

from flask_mail import Message
from app import mail
from app import limiter

@main.route('/contact', methods=['POST'])
@limiter.limit("2 per second")
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    msg = Message(subject="Nouveau message de contact",
                  sender=email,
                  recipients=["ton.email@gmail.com"],  # ton adresse
                  body=f"Nom : {name}\nTéléphone : {phone}\nEmail : {email}")

    try:
        mail.send(msg)
        flash("Message envoyé avec succès !", "success")
    except Exception as e:
        flash("Erreur lors de l'envoi : " + str(e), "danger")

    return redirect(url_for('main.home'))