import os

basedir = os.path.abspath(os.path.dirname(__file__))

API_URL = "http://localhost:5000/v1/trades"

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../resources/trades.db')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'