from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_login import LoginManager
import cloudinary
import os

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()
login_manager = LoginManager()

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
    login_manager.init_app(app)   # Login Manager Initialization

    # Cloudinary Initialization
    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET'],
        secure=True
    )

    from app.models import User

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

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
    from app.blueprints.ai_chat.routes import chat_bp
    from app.blueprints.gallery.routes import gallery_bp
    from app.blueprints.api import api_bp
    from app.blueprints.api import auth_routes, todo_routes

    csrf.exempt(api_bp)

    app.register_blueprint(about_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(ideas_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(api_bp)

    return app
