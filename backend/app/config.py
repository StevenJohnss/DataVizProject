import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # JWT_SECRET_KEY gets used automatically by JWTManager
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 'stev_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:1234@localhost:5432/dataviz'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
