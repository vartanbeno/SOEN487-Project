class Config(object):
    SQLALCHEMY_DATABASE_URI = r"sqlite:///notification_microservice.sqlite"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///tests/test_notification_microservice.sqlite"