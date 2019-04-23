import datetime

class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///SOEN487_API.sqlite"
    JWT_SECRET_KEY = 'teamgiovanniprattico'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///tests/test_SOEN487_API.sqlite"
    JWT_SECRET_KEY = 'teamgiovanniprattico'
    JWT_EXPIRES = datetime.timedelta(days=1)