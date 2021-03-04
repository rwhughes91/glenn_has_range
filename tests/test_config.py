from flask import Flask

from config import config_by_name


class TestDevelopmentConfig:
    def test_app_is_development(self, app: Flask) -> None:
        """To ensure development configurations are passed to app"""

        test_config = config_by_name["dev"]
        app.config.from_object(test_config)

        assert app.config["DEBUG"] is True
        assert app.config["TESTING"] is False
        assert app.config["ENV"] == "development"


class TestProductionConfig:
    def test_app_is_production(self, app: Flask) -> None:
        """To ensure production configurations are passed to app"""

        test_config = config_by_name["prod"]
        app.config.from_object(test_config)

        assert app.config["DEBUG"] is False
        assert app.config["TESTING"] is False
        assert app.config["ENV"] == "production"


class TestTestingConfig:
    def test_app_is_testing(self, app: Flask) -> None:
        """To ensure testing configurations are passed to app"""

        test_config = config_by_name["test"]
        app.config.from_object(test_config)

        assert app.config["DEBUG"] is True
        assert app.config["TESTING"] is True
        assert app.config["ENV"] == "testing"
