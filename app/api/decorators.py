from functools import wraps
from typing import Callable
from flask_restplus import Api
from flask import request, g

from .errors import BadRequest
from .models import User


def expect_jwt(
    api: Api,
    message: str = "JWT token is required and has the format: 'Bearer <token>'",
) -> Callable:
    """
    Adds expected header to swagger,
    validates JWT token is present,
    adds token to g
    """

    def decorator(func: Callable) -> Callable:
        """Adds expected header to swagger"""

        @api.response(403, message)
        @api.header(
            "Authorization",
            "JWT token to authorize request. Example: 'Bearer <my token>'",
        )
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            """
            validates JWT token is present,
            adds token to g
            """

            auth = request.headers.get("Authorization")

            if not auth:
                raise BadRequest(
                    "Unauthorized",
                    401,
                    {"Request.Header.Authorization": "JWT token is required"},
                )

            auth_list = auth.split(" ")
            if len(auth_list) != 2:
                raise BadRequest(
                    "Invalid Auth Header",
                    400,
                    {"Authorization": "JWT token has the format: 'Bearer <token>'"},
                )

            token = auth_list[1]
            payload = User.decode_auth_token(token)

            # attaching token and payload to app context
            g.token = token
            g.payload = payload

            return func(*args, **kwargs)

        return wrapper

    return decorator


def admin(func: Callable) -> Callable:
    """Raises BadRequest exception if user is not admin"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        """
        validates JWT Payload is present,
        validates user is admin
        """

        payload = g.payload

        if not isinstance(payload, int):
            raise BadRequest(
                "Unauthorized",
                401,
                {"Request.Header.Authorization": "JWT token is required"},
            )

        user = User.query.filter_by(user_id=payload).first()

        if not user.admin:
            raise BadRequest(
                "Forbidden", 403, {"error_message": "This route is protected to admins"}
            )

        return func(*args, **kwargs)

    return wrapper
