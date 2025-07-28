import os
from dotenv import load_dotenv

load_dotenv()   # Ensures that environment is loaded before accessing any variables to resolve SQLALCHEMY_DATABASE_URI error

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
