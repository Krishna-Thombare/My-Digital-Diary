import os
from dotenv import load_dotenv

load_dotenv()   # Ensures that environment is loaded before accessing any variables to resolve SQLALCHEMY_DATABASE_URI error

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret')
    
    # Database Info
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    
    # Database URI
    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl_mode=REQUIRED"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
