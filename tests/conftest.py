import pytest
from typing import Iterator, Any
from flask import Flask

from app import create_app, db


@pytest.fixture
def app() -> Iterator[Flask]:
    """Create application for the tests"""

    _app = create_app("test")

    with app.app_context():
        db.create_all()

    db.session.close()
    db.drop_all()

    yield _app


@pytest.fixture
def client(app: Flask) -> Iterator[Any]:
    """Creates the testing client"""

    yield app.test_client()
