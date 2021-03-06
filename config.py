from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

if not environ.get("SECRET_KEY"):
    raise Exception("ENV variable SECRET_KEY must be set")

if not environ.get("DATABASE_URI"):
    raise Exception("ENV variable DATABASE_URI must be set")


class Config:
    """Base config class for application factory"""

    SECRET_KEY = environ.get("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATESS_FOLDER = "templates"
    SERVER_NAME = environ.get("SERVER_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class DevConfig(Config):
    """Dev config class for application factory"""

    ENV = "development"
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URI")


class TestConfig(Config):
    """Test config class for application factory"""

    ENV = "testing"
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class ProdConfig(Config):
    """Prod config class for application factory"""

    ENV = "production"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URI")


config_by_name = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}

key = Config.SECRET_KEY
