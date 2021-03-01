from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from flask_restplus import Namespace, fields

from app import db


class PlaylistDto:
    """Playlist data transfer object"""

    api = Namespace("playlist", description="Spotify playlist operations")
    playlist = api.model(
        "playlist",
        {
            "id": fields.String(description="playlist identifier"),
            "datasource": fields.String(
                required=True, description="playlist data source"
            ),
            "screen_name": fields.String(
                required=True, description="playlist screen name"
            ),
            "playlist_link": fields.String(
                required=True, description="link to visit playlist"
            ),
            "playlist_description": fields.String(description="playlist description"),
        },
    )


class Playlist(db.Model):
    """Data model for Spotify playlists"""

    __tablename__ = "spotify_playlists"
    __table_args__ = {"schema": "spotify_playlists"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    datasource = Column(db.String)
    screen_name = Column(db.String, nullable=False)
    playlist_link = Column(db.String, nullable=False)
    playlist_description = Column(db.Text)
    last_update = Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f"<Playlist {self.playlist_link}>"
