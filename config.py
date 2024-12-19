import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///main.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'tr']  # Desteklenen diller
    BABEL_DEFAULT_LOCALE = 'en'  # Varsayılan dil
    BABEL_DEFAULT_TIMEZONE = 'UTC'  # Varsayılan zaman dilimi

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
