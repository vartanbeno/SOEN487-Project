class Config(object):
    SQLALCHEMY_DATABASE_URI = r"sqlite:///conversations.sqlite"
    SECRET_KEY="Noodles"


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///tests/test_SOEN487_A1.sqlite"