from app import create_app


class TestTestingConfig:
    def test_app_is_testing(self) -> None:
        """To ensure testing configurations are passed to app"""

        app = create_app("test")
        assert app.config["DEBUG"] is True
        assert app.config["TESTING"] is True
        assert app.config["ENV"] == "testing"
        assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"


class TestDevelopmentConfig:
    def test_app_is_development(self) -> None:
        """To ensure development configurations are passed to app"""

        app = create_app("dev")
        assert app.config["DEBUG"] is True
        assert app.config["TESTING"] is False
        assert app.config["ENV"] == "development"


class TestProductionConfig:
    def test_app_is_production(self) -> None:
        """To ensure production configurations are passed to app"""

        app = create_app("prod")
        assert app.config["DEBUG"] is False
        assert app.config["TESTING"] is False
        assert app.config["ENV"] == "production"
