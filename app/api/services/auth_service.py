from app import db

from ..models import User, BlacklistToken
from ..errors import BadRequest


def save_token(token: str) -> bool:
    """Saves the token to the token blacklist table"""

    blacklist_token = BlacklistToken(token)
    try:
        db.session.add(blacklist_token)
        db.session.commit()
        return True
    except Exception as e:
        raise BadRequest(
            "There was an error logging out. Please try again.",
            500,
            {"error_message": str(e)},
        )


def login_user(auth_data) -> str:
    """Logs in the user"""

    try:
        user = User.query.filter_by(email=auth_data["email"]).first()

        if user and user.check_password(auth_data["password"]):
            return user.encode_auth_token(user.user_id)

        raise BadRequest("Email or password do not match", 401)

    except BadRequest as e:
        raise e

    except Exception as e:
        raise BadRequest(
            "There was an error logging in. Please try again.",
            500,
            {"error_message": str(e)},
        )


def logout_user(token: str, payload: int) -> bool:
    """Logs the user out"""

    try:
        if isinstance(payload, int):
            return save_token(token)

        else:
            raise Exception("Error decoding your token")

    except BadRequest as e:
        raise e

    except Exception as e:
        raise BadRequest(
            "There was an error logging out", 500, {"error_message": str(e)}
        )


def generate_token(user: User) -> str:
    """Generates an auth token based on user's ID"""

    try:
        return user.encode_auth_token(user.id)

    except Exception as e:
        raise BadRequest(
            "Some error occurred. Please try again.", 404, {"error_message": str(e)}
        )
