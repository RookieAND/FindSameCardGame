import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'minigameweb'
    SECURITY_PASSWORD_SALT = 'minigamepwsalt'


class DevelopmentConfig(Config):
    DEBUG = True

    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


class ProductionConfig(Config):
    DEBUG = False

    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_POST = os.environ.get('MAIL_POST')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
