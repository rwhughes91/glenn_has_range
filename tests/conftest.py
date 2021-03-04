import pytest
from typing import Iterator, Any
from flask import Flask
from datetime import datetime

from app import create_app, db
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
    }
]


@pytest.fixture
def app() -> Iterator[Flask]:
    """Create application for the tests"""

    _app = create_app("test")

    with app.app_context():
        db.create_all()

        # seed playlist table
        playlists_obj = []
        for playlist in playlists:
            playlists_obj.append(Playlist(**playlist))
        db.session.add_all(playlists_obj)

        # seed user table
        users_obj = []
        for user in users:
            users_obj.append(User(**user))
        db.session.add_all(users_obj)

        db.session.commit()

    db.session.close()
    db.drop_all()

    yield _app


@pytest.fixture
def client(app: Flask) -> Iterator[Any]:
    """Creates the testing client"""

    yield app.test_client()
