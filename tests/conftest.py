import pytest

from typing import Any, Callable, Dict
from flask import Flask
from datetime import datetime

from app import create_app, db as _db
from app.api.models import Playlist, User


playlists = [
    {
        "playlist_id": "a600f327-a53c-4d2d-8d31-41f5a8b81121",
        "datasource": "reddit",
        "screen_name": "name1",
        "playlist_link": "https://somelink1.com",
        "playlist_description": "First description",
    },
    {
        "playlist_id": "5214cef2-a7f7-4d46-a95d-93ff0e2d9382",
        "datasource": "reddit",
        "screen_name": "name2",
        "playlist_link": "https://somelink2.com",
    },
    {
        "playlist_id": "87569b1d-8975-4522-97a4-039346c53512",
        "datasource": "reddit",
        "screen_name": "name3",
        "playlist_link": "https://somelink3.com",
        "playlist_description": "This is a description",
    },
]

users = [
    {
        "email": "someEmail@google.com",
        "username": "someEmail@google.com",
        "password": "testPasssword@123",
        "registered_on": datetime.utcnow(),
        "public_id": "9a2a2576-1683-4cb4-aa15-10728dd83ac9",
        "admin": True,
    }
]


@pytest.fixture(scope="module")
def app() -> Flask:
    """Create application for the tests"""

    _app = create_app("test")
    _app.app_context().push()

    return _app


@pytest.fixture(scope="module")
def client(app: Flask) -> Any:
    """Creates the testing client"""

    return app.test_client()


@pytest.fixture(scope="module")
def db(app: Flask) -> _db:
    """Seeds the database for tests"""

    with app.app_context():
        _db.create_all()

        # seed playlist table
        playlists_obj = []
        for playlist in playlists:
            playlists_obj.append(Playlist(**playlist))
        _db.session.add_all(playlists_obj)

        # seed user table
        users_obj = []
        for user in users:
            users_obj.append(User(**user))

        _db.session.add_all(users_obj)
        _db.session.commit()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture(scope="module")
def client_request(client, db) -> Callable:
    """Sets up JWT Headers for client testing"""

    auth = {
        "email": "someEmail@google.com",
        "password": "testPasssword@123",
    }
    res = client.post("/api/auth/login", json=auth)
    token = res.json["Authorization"]

    def send_request(
        endpoint: str, method: str = "get", payload: Dict[str, Any] = None
    ) -> None:
        """Sends request using test client"""

        return getattr(client, method)(
            endpoint, json=payload, headers={"Authorization": f"Bearer {token}"}
        )

    return send_request
