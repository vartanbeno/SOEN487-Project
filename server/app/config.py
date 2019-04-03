import datetime
import os
import secrets

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

DB = os.path.join(CURRENT_DIR, 'SOEN487_Project.sqlite')
TEST_DB = os.path.join(CURRENT_DIR, 'tests', 'test_SOEN487_Project.sqlite')


class Config(object):
    # JWT secret key is randomly generated each time the app is run
    JWT_SECRET_KEY = secrets.token_hex(32)
    JWT_EXPIRES = datetime.timedelta(days=30)
    SQLALCHEMY_DATABASE_URI = fr'sqlite:///{DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = fr'sqlite:///{TEST_DB}'
