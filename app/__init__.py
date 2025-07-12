from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
import os

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    load_dotenv()  # Loads from .env

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

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
