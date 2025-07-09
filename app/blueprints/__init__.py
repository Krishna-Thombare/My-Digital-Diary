from flask import Flask
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.form_object('config.Config')
    
    db.init_app(app)
    
    from app.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    return app