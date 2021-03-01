from app import db
from ..models import User, BlacklistToken
from ..errors import BadRequest


def save_token(token: str):
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
            dict(error_message=e),
        )


def login_user(auth_data) -> str:
    """Logs in the user"""

    try:
        user = User.query.filter_by(email=auth_data["email"]).first()
        if user and user.check_password(auth_data["password"]):
            return user.encode_auth_token(user.id)

        raise BadRequest("Email or password do not match", 401)

    except Exception as e:
        raise BadRequest(
            "There was an error logging in. Please try again.",
            500,
            dict(error_message=e),
        )


def logout_user(auth_data):
    """Logs the user out"""

    auth_token = auth_data.split(" ")[1] if auth_data else ""
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            # mark the token as blacklisted
            return save_token(auth_token)
        else:
            raise BadRequest("There was an error logging out", 401, dict(message=resp))
    else:
        raise BadRequest("Provide a valid auth token", 403)


def generate_token(user: User) -> str:
    """Generates an auth token based on user's ID"""

    try:
        return user.encode_auth_token(user.id)

    except Exception as e:
        raise BadRequest(
            "Some error occurred. Please try again.", 404, dict(error_message=e)
        )
