# Loan Eligibility App

Une application web permettant d'évaluer l’éligibilité d’un utilisateur à un prêt bancaire en fonction de son profil. L’application fournit une prédiction instantanée, une justification en cas de refus, et une interface d’administration avec historique des demandes.

---

## 🚀 Fonctionnalités

- Formulaire dynamique en plusieurs étapes
- Prédiction basée sur un modèle de machine learning (régression logistique)
- Justification des refus (DTI, revenu, antécédents…)
- Base de données locale (SQLite)
- Interface admin avec export Excel
- Formulaire de contact avec envoi d’e-mail
- Limitation anti-spam sur les requêtes

---

## 🛠️ Technologies utilisées

- Python, Flask, Flask-SQLAlchemy
- Scikit-learn, Pandas, Joblib
- Flask-Mail, Flask-Limiter
- HTML / Tailwind CSS / JavaScript

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/10969shirazu/loan-eligibility-app
cd loan-eligibility-app
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables (optionnel pour Flask-Mail)

Dans `app/__init__.py`, configurer :

```python
MAIL_USERNAME = 'votre.email@gmail.com'
MAIL_PASSWORD = 'mot_de_passe_app'
```

---

## 🧪 Initialiser la base de données

```bash
python create_db.py
```

---

## ▶️ Lancer l’application

```bash
flask run
```

Par défaut, le site sera accessible sur : http://127.0.0.1:5000

---

## 👤 Accéder à l'interface admin

```
http://127.0.0.1:5000/admin/requests
```

---

## 📂 Arborescence simplifiée

```
loan-eligibility-app/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── model/
│   ├── templates/
│   └── static/
├── create_db.py
├── test_m.py
├── requirements.txt
└── README.md
```

---

## ✅ Contributions

Projet universitaire – non destiné à une utilisation en production.
Contributions bienvenues pour amélioration ou déploiement cloud !
