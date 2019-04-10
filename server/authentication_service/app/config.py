import datetime
import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

DB = os.path.join(CURRENT_DIR, 'SOEN487_Project.sqlite')
TEST_DB = os.path.join(CURRENT_DIR, 'tests', 'test_SOEN487_Project.sqlite')


class Config(object):
    JWT_SECRET_KEY = 'teamgiovanniprattico'
    JWT_EXPIRES = datetime.timedelta(days=1)
    SQLALCHEMY_DATABASE_URI = fr'sqlite:///{DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = fr'sqlite:///{TEST_DB}'
