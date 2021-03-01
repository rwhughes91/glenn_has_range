from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from app import db


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
