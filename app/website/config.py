class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'SECRET_KEY'
    DB_NAME = "database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'


class TestConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
