from flask import Flask, render_template, request, session
import numpy as np
import os
import cloudpickle
import joblib
import matplotlib.pyplot as plt
import shap


current_dir = os.path.dirname(os.path.abspath(__file__)) 
model_path = os.path.join(current_dir, "models/loan_model_reg3.pkl") 
model_scal = os.path.join(current_dir, "models/scaler3.pkl") 
model_exp = os.path.join(current_dir, "models/explainer3.pkl") 
model_mean = os.path.join(current_dir, "models/meanpos3.pkl")
model = joblib.load(model_path) 
scaler = joblib.load(model_scal)
meanpos = joblib.load(model_mean)

with open(model_exp, 'rb') as f:
    explainer = cloudpickle.load(f)

required_columns = [
    "loan_amnt","term", "int_rate", "installment", "grade", "sub_grade", 
    "emp_length", "annual_inc", "dti", "delinq_2yrs",
    "inq_last_6mths", "open_acc", "pub_rec", "revol_bal", "revol_util",
    "total_acc", "last_pymnt_amnt", "home_ownership_MORTGAGE", "home_ownership_NONE",
    "home_ownership_OTHER", "home_ownership_OWN", "home_ownership_RENT", 
    "verification_status_Source Verified", "verification_status_Verified",
    "purpose_credit_card", "purpose_debt_consolidation", "purpose_educational",
    "purpose_home_improvement", "purpose_house", "purpose_major_purchase",
    "purpose_medical", "purpose_moving", "purpose_other", "purpose_renewable_energy",
    "purpose_small_business", "purpose_vacation", "purpose_wedding"
]

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=["GET"])
def acceuil():
    return render_template("index.html")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == "POST":
        vals = [
            int(request.form.get("loan_amnt")),
            int(request.form.get("term")),
            int(request.form.get("int_rate")),
            int(request.form.get("installment")),
            int(request.form.get("grade")),
            int(request.form.get("sub_grade")),
            int(request.form.get("emp_length")),
            int(request.form.get("annual_inc")),
            int(request.form.get("dti")),
            int(request.form.get("delinq_2yrs")),
            int(request.form.get("inq_last_6mths")),
            int(request.form.get("open_acc")),
            int(request.form.get("pub_rec")),
            int(request.form.get("revol_bal")),
            int(request.form.get("revol_util")),
            int(request.form.get("total_acc")),
            int(request.form.get("last_pymnt_amnt"))
        ]

        home_ownership_options = ["MORTGAGE", "NONE", "OTHER", "OWN", "RENT"]
        home_vals = [1 if ho in request.form.getlist("home_ownership") else 0 for ho in home_ownership_options]

        verif_options = ["Source Verified", "Verified"]
        verif_vals = [1 if vs in request.form.getlist("verification_status") else 0 for vs in verif_options]

        purpose_options = [
            "credit_card", "debt_consolidation", "educational", "home_improvement", "house",
            "major_purchase", "medical", "moving", "other", "renewable_energy",
            "small_business", "vacation", "wedding"
        ]

        purpose_vals = [1 if purp in request.form.getlist("purpose") else 0 for purp in purpose_options]

        data = np.array([vals + home_vals + verif_vals + purpose_vals], dtype=float)
        session["data"] = data.tolist()
        data_scaled = scaler.transform(data)
        prediction = model.predict(data_scaled)[0]
 
        session["data_scaled"] = data_scaled.tolist()
        return render_template("result.html", prediction=prediction)
    else:
        return render_template("form.html")

@app.route("/why", methods=["GET"])
def explain():
    data_scaled = np.array(session["data_scaled"])

    data = np.array(session["data"])

    shap_values = explainer.shap_values(data_scaled)

    contributions = dict(zip(required_columns, shap_values[0]))

    negative_contributions = {k: v for k, v in contributions.items() if v < 0}

    sorted_negative_contributions = sorted(negative_contributions.items(), key=lambda x: abs(x[1]), reverse=True)

    resu = []
    for var, contr in sorted_negative_contributions:
        mean = meanpos.get(var)
        introd = data[0][required_columns.index(var)] if var in required_columns else None
        resu.append({
            "variable": var,
            "score": contr,
            "mean": mean,
            "val": introd
        })

    plt.figure()
    shap.summary_plot(shap_values, data_scaled, feature_names=required_columns, show=False)
    #plt.show()
    categ = ["home_ownership_MORTGAGE", "home_ownership_NONE",
    "home_ownership_OTHER", "home_ownership_OWN", "home_ownership_RENT", 
    "verification_status_Source Verified", "verification_status_Verified",
    "purpose_credit_card", "purpose_debt_consolidation", "purpose_educational",
    "purpose_home_improvement", "purpose_house", "purpose_major_purchase",
    "purpose_medical", "purpose_moving", "purpose_other", "purpose_renewable_energy",
    "purpose_small_business", "purpose_vacation", "purpose_wedding"]

    return render_template("explain.html", why=resu[:5], categ = categ)

if __name__ == '__main__':
    app.run(debug=True)
