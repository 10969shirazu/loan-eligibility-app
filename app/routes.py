from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@main.route('/predict', methods=['POST'])
def predict():
    name = request.form.get("name")
    income = float(request.form.get("income"))
    age = int(request.form.get("age"))
    job_type = request.form.get("job_type")

    # Appelle du modèle ML
    eligible = income > 2000 and age > 18  # Remplace vrai modèle

    return render_template("result.html", name=name, eligible=eligible)
