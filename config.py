from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Base config class for appliction factory"""

    SECRET_KEY = environ.get("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATESS_FOLDER = "templates"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class DevConfig(Config):
    """Dev config class for appliction factory"""

    ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get("DEV_DATABASE_URI")


class TestConfig(Config):
    """Test config class for appliction factory"""

    ENV = "testing"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get("TEST_DATABASE_URI")
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProdConfig(Config):
    """Prod config class for appliction factory"""

    ENV = "production"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get("PROD_DATABASE_URI")


config_by_name = dict(dev=DevConfig, test=TestConfig, prod=ProdConfig)

key = Config.SECRET_KEY
