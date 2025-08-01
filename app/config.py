import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}