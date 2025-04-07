from flask import Flask, render_template, request, session
import numpy as np
import os
import cloudpickle
import joblib
import matplotlib.pyplot as plt
import shap


current_dir = os.path.dirname(os.path.abspath(__file__)) 
model_path = os.path.join(current_dir, "models/logistic_model.pkl") 
model_scal = os.path.join(current_dir, "models/scaler.pkl") 
model_exp = os.path.join(current_dir, "models/explainer.pkl") 
model_mean = os.path.join(current_dir, "models/meanpos.pkl")
model = joblib.load(model_path) 
scaler = joblib.load(model_scal)
meanpos = joblib.load(model_mean)


with open(model_exp, 'rb') as f:
    explainer = cloudpickle.load(f)

required_columns = [
            "loan_amnt","term", "int_rate", "annual_inc", "dti", "delinq_2yrs",
            "inq_last_6mths", "open_acc", "pub_rec", "revol_bal", "revol_util",
            "total_acc", "last_pymnt_amnt", "RENT", "OWN",
            "Source Verified", "Verified",
            "credit_card", "debt_consolidation", "home_improvement",
            "major_purchase", "medical", "other", "small_business"
        ]

app = Flask(__name__)
app.secret_key = "0a5182143ef857c588fad8223df8b2c9e9d03fff1555b13a11025e6fba88c864"

@app.route('/', methods=["GET"])
def acceuil():
    return render_template("index.html")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == "POST":
        val1 = float(request.form.get("loan_amnt"))
        val2 = float(request.form.get("term"))
        val3 = float(request.form.get("int_rate"))
        val4 = float(request.form.get("annual_inc"))
        val5 = float(request.form.get("dti"))
        val6 = float(request.form.get("delinq_2yrs"))
        val7 = float(request.form.get("inq_last_6mths"))
        val8 = float(request.form.get("open_acc"))
        val9 = float(request.form.get("pub_rec"))
        val10 = float(request.form.get("revol_bal"))
        val11 = float(request.form.get("revol_util"))
        val12 = float(request.form.get("total_acc"))
        val13 = float(request.form.get("last_pymnt_amnt"))




        # Statut de propriété (checkbox)
        home_ownership_own = 0 if "OWN" in request.form.getlist("home_ownership") else 1
        home_ownership_rent = 0 if "RENT" in request.form.getlist("home_ownership") else 1


        # Statut de vérification (checkbox)
        verif_source_verified = 0 if "Source Verified" in request.form.getlist("verification_status") else 1
        verif_verified = 0 if "Verified" in request.form.getlist("verification_status") else 1


        # Objet du prêt (checkbox)
        purpose_credit_card = 0 if "credit_card" in request.form.getlist("purpose") else 1
        purpose_debt_consolidation = 0 if "debt_consolidation" in request.form.getlist("purpose") else 1
        purpose_home_improvement = 0 if "home_improvement" in request.form.getlist("purpose") else 1
        purpose_major_purchase = 0 if "major_purchase" in request.form.getlist("purpose") else 1
        purpose_medical = 0 if "medical" in request.form.getlist("purpose") else 1
        purpose_other = 0 if "other" in request.form.getlist("purpose") else 1
        purpose_small_business = 0 if "small_business" in request.form.getlist("purpose") else 1


        # Préparation des données pour la prédiction
        data = np.array([[val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, 
                          val11, val12, val13, home_ownership_own, home_ownership_rent, 
                          verif_source_verified, verif_verified, purpose_credit_card, 
                          purpose_debt_consolidation, purpose_home_improvement, 
                          purpose_major_purchase, purpose_medical, purpose_other, 
                          purpose_small_business]], dtype=float)

        session["data"]=data.tolist()
        data_scaled = scaler.transform(data) 

        prediction = model.predict(data_scaled)[0]
        print("\n\n\n",prediction)
        return render_template("result.html", prediction = prediction)
    else :
        return render_template("form.html")


@app.route("/why", methods=["GET"])
def explain():
    data = np.array(session["data"], dtype=float)
    shap_values = explainer(data)

    contributions = dict(zip(required_columns, shap_values.values[0]))
    negative_contributions = {k: v for k, v in contributions.items() if v < 0}
    sorted_negative_contributions = sorted(negative_contributions.items(), key=lambda x: abs(x[1]), reverse=True)
  
    resu = []
    for var, contr in sorted_negative_contributions:
        mean = meanpos.get(var)
        introd = data[0][required_columns.index(var)]
 
        resu.append({
            "variable":var,
            "score":contr,
            "mean":mean,
            "val":introd
        })
    print("\n\n\n", resu)

    
    plt.figure(figsize=(10,5))
    shap.summary_plot(shap_values,data, feature_names = required_columns)
    plt.show()
    
    return render_template("explain.html", why=resu[:5])


if __name__ == '__main__':
    app.run(debug=True)