from typing import List, Dict, Any
from uuid import UUID
from datetime import datetime

from app import db
from ..models import Playlist
from ..errors import BadRequest


def get_playlists(
    search: str = None, filters: Dict[str, Any] = None, limit: int = None, skip: int = 0
) -> List[Playlist]:
    """Gets all the playlists"""

    query = Playlist.query.filter_by(**filters["fields"])

    if search:
        query = query.search(search)

    query = query.offset(skip)
    if limit:
        query = query.limit(limit)

    return query.all()


def get_playlist(playlist_id: str) -> Playlist:
    """Gets a playlist"""

    validate_playlist_id(playlist_id)
    playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
    if not playlist:
        raise BadRequest("Playlist doesn't exist", 404)
    return playlist


def put_playlist(playlist_id: str, playlist_data, created_by: int) -> Playlist:
    """Edits or creates a playlist based on passed playlist_id"""

    validate_playlist_id(playlist_id)
    playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
    try:
        if playlist:
            # edit the current playlist
            for key, value in playlist_data.items():
                setattr(playlist, key, value)
            db.session.commit()
            return playlist
        else:
            # create a new playlist
            new_playlist = Playlist(
                datasource=playlist_data["datasource"],
                screen_name=playlist_data["screen_name"],
                playlist_link=playlist_data["playlist_link"],
                playlist_description=playlist_data.get("playlist_description", ""),
                last_update=datetime.utcnow(),
                created_by=created_by,
            )
            save_changes(new_playlist)
            return new_playlist
    except Exception as e:
        raise BadRequest(
            "There was an error editing your playlist", 400, {"error_message": str(e)}
        )


def save_new_playlist(playlist_data, created_by: int) -> Playlist:
    """Creates a new playlist"""

    playlist = Playlist.query.filter_by(
        playlist_link=playlist_data["playlist_link"]
    ).first()
    if not playlist:
        new_playlist = Playlist(
            datasource=playlist_data["datasource"],
            screen_name=playlist_data["screen_name"],
            playlist_link=playlist_data["playlist_link"],
            playlist_description=playlist_data.get("playlist_description", ""),
            last_update=datetime.utcnow(),
            created_by=created_by,
        )
        save_changes(new_playlist)
        return new_playlist

    raise BadRequest(
        "Playlist already exists",
        400,
        {"playlist_link": "playlist_link must be unique"},
    )


def validate_playlist_id(playlist_id: str) -> bool:
    """Validates the passed string is a valid UUID"""
    try:
        UUID(playlist_id)
        return True
    except ValueError:
        raise BadRequest("Playlist identifier must be a valid UUID")


def save_changes(data: Playlist) -> None:
    """Adds data to session and saves to DB"""

    db.session.add(data)
    db.session.commit()
