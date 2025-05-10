from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"], storage_uri="memory://")

mail = Mail()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loan_requests.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuration SMTP (exemple pour Gmail)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = ''      
    app.config['MAIL_PASSWORD'] = ''     
    mail.init_app(app)
    
    #Limiter l'envoi des mails pour éviter les spams
    limiter.init_app(app)
    
    #Chargement du model
    from .models import db as model_db 
    model_db.init_app(app)

    from .routes import main
    app.register_blueprint(main)
    
    __all__ = ['db', 'mail', 'limiter']

    return app
