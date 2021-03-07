from typing import Dict, Any

from app import create_app, db
from app.api import api
from app.api.models import Playlist, User, BlacklistToken
from datetime import datetime

app = create_app("dev")
app.app_context().push()


playlists = [
    {
        "playlist_id": "a600f327-a53c-4d2d-8d31-41f5a8b81121",
        "datasource": "reddit",
        "screen_name": "name1",
        "playlist_link": "https://somelink1.com",
        "playlist_description": "First description",
        "created_by": 1,
    },
    {
        "playlist_id": "5214cef2-a7f7-4d46-a95d-93ff0e2d9382",
        "datasource": "reddit",
        "screen_name": "name2",
        "playlist_link": "https://somelink2.com",
        "created_by": 1,
    },
    {
        "playlist_id": "87569b1d-8975-4522-97a4-039346c53512",
        "datasource": "reddit",
        "screen_name": "name3",
        "playlist_link": "https://somelink3.com",
        "playlist_description": "This is a description",
        "created_by": 1,
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


@app.shell_context_processor
def make_shell_context() -> Dict[str, Any]:
    """Make objects available during shell"""

    return {
        "db": db,
        "api": api,
        "Playlist": Playlist,
        "User": User,
        "BlacklistToken": BlacklistToken,
        "playlists": playlists,
        "users": users,
    }


if __name__ == "__main__":
    app.run(port=5000)
