from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from flask_mail import Mail
import os

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()

def create_app():
    load_dotenv()  # Loads from .env

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object('config.Config')
    
    # Mail Configuration - (To receive users contact us messages)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')   # 16-Digit App Password (*Not Gmail Password*)
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    db.init_app(app)              # Database Initilization
    migrate.init_app(app, db)     # Database Migration Initilization
    csrf.init_app(app)            # CSRF Token Initilization
    mail.init_app(app)            # Mail Initialization

    # Import and register blueprints
    from app.blueprints.about.routes import about_bp
    from app.blueprints.home.routes import home_bp
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.journal.routes import journal_bp
    from app.blueprints.notes.routes import notes_bp
    from app.blueprints.quotes.routes import quotes_bp
    from app.blueprints.ideas.routes import ideas_bp
    from app.blueprints.todo.routes import todo_bp
    from app.blueprints.contact.routes import contact_bp

    app.register_blueprint(about_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(ideas_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(contact_bp)

    return app
