import uuid
from typing import List
from datetime import datetime
from sqlalchemy import or_

from app import db
from ..models import User
from ..errors import BadRequest


def get_users() -> List[User]:
    """Gets all the users"""

    return User.query.all()


def get_user(public_id: str) -> User:
    """Gets a user"""

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        raise BadRequest("User doesn't exist", 404)
    return user


def save_new_user(user_data) -> User:
    """Creates a new user"""
    user = User.query.filter(
        or_(User.email == user_data["email"], User.username == user_data["username"])
    ).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=user_data["email"],
            username=user_data["username"],
            password=user_data["password"],
            admin=user_data.get("admin"),
            registered_on=datetime.utcnow(),
        )
        save_changes(new_user)
        return new_user
    raise BadRequest("User already exists")


def save_changes(data: User) -> None:
    """Adds data to session and saves to DB"""

    db.session.add(data)
    db.session.commit()
