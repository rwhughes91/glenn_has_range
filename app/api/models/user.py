from sqlalchemy import Column
from flask_restplus import Namespace, fields

from app import db, flask_bcrypt


class UserDto:
    """User data transfer object"""

    api = Namespace("user", description="user related operations")
    user = api.model(
        "user",
        {
            "email": fields.String(required=True, description="user email address"),
            "username": fields.String(required=True, description="user username"),
            "password": fields.String(required=True, description="user password"),
            "public_id": fields.String(description="user Identifier"),
        },
    )


class User(db.Model):
    """User model for storing users"""

    __tablename__ = "user"
    __table_args__ = {"schema": "spotify_playlists"}

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    @property
    def password(self) -> str:
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

    def check_password(self, password: str) -> bool:
        """Confirms password to saved hash"""

        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
