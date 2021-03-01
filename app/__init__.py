from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


from config import config_by_name

db = SQLAlchemy()
migrate = Migrate()
flask_bcrypt = Bcrypt()


def create_app(config_name: str):
    """Initialize the core application"""

    app = Flask(__name__, instance_relative_config=False)
    configure_app(app, config_name)

    with app.app_context():
        configure_extensions(app)
        configure_blueprints(app)
        return app


def configure_app(app: Flask, config_name: str):
    """Different ways of configurations"""

    config = config_by_name[config_name]
    app.config.from_object(config)


def configure_extensions(app: Flask):
    """Configure extensions for app"""

    db.init_app(app)
    migrate.init_app(app, db)
    flask_bcrypt.init_app(app)


def configure_blueprints(app: Flask):
    """Configure blueprints in views"""

    from .api import api_blueprint

    for bp in [api_blueprint]:
        app.register_blueprint(bp)
