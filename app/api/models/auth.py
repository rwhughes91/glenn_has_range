from datetime import datetime
from sqlalchemy import Column
from flask_restplus import Namespace, fields

from app import db


class BlacklistToken(db.Model):
    """Token modal for storing JWT Tokens"""

    __tablename__ = "blacklist_tokens"

    token_id = Column(db.Integer, primary_key=True, autoincrement=True)
    token = Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = Column(db.DateTime, nullable=False)

    def __init__(self, token: str) -> None:
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self) -> str:
        return f"<id: token: {self.token}"

    @staticmethod
    def check_blacklist(token: str) -> bool:
        """Check whether auth token has been blacklisted"""

        res = BlacklistToken.query.filter_by(token=token).first()
        return bool(res)


class AuthDto:
    """Auth data transfer object"""

    api = Namespace("auth", description="authentication related operations")
    user_auth = api.model(
        "auth_details",
        {
            "email": fields.String(required=True, description="The email address"),
            "password": fields.String(required=True, description="The user password"),
        },
    )
