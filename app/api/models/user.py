from datetime import datetime, timedelta
from sqlalchemy import Column
from flask_restplus import Namespace, fields
import jwt


from app import db, flask_bcrypt
from config import key
from ..errors import BadRequest
from .auth import BlacklistToken


class User(db.Model):
    """User model for storing users"""

    __tablename__ = "users"

    user_id = Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    playlists = db.relationship("Playlist", backref="playlists", lazy=True)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

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

    def encode_auth_token(self, user_id: str) -> str:
        """Generates the auth token"""

        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=1, seconds=5),
                "iat": datetime.utcnow(),
                "sub": user_id,
            }
            token = jwt.encode(payload, key or "", algorithm="HS256")
            return str(token)

        except Exception as e:
            raise BadRequest(
                "There was an error encoding the auth token",
                500,
                {"error_message": str(e)},
            )

    @staticmethod
    def decode_auth_token(auth_token: str) -> str:
        """Decodes the auth token"""

        try:
            payload = jwt.decode(auth_token, key or "", algorithms="HS256")
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                raise BadRequest("Token blacklisted. Please log in again.")
            else:
                return payload["sub"]

        except jwt.ExpiredSignatureError:
            raise BadRequest("Signature expired. Please log in again.")

        except jwt.InvalidTokenError:
            raise BadRequest("Invalid token. Please log in again.")


class UserDto:
    """User data transfer object"""

    api = Namespace("user", description="user related operations")
    user = api.model(
        "user",
        {
            "email": fields.String(required=True, description="user email address"),
            "username": fields.String(required=True, description="user username"),
            "password": fields.String(required=True, description="user password"),
            "public_id": fields.String(description="user identifier"),
        },
    )
