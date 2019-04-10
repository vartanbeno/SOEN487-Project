import datetime


class Config(object):
    JWT_SECRET_KEY = 'teamgiovanniprattico'
    JWT_EXPIRES = datetime.timedelta(days=1)
    SQLALCHEMY_DATABASE_URI = r"sqlite:///notification_microservice.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///tests/test_notification_microservice.sqlite"
