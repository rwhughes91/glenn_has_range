from .decorators import run_only_once
from ..models import User
from ..errors import BadRequest


class AuthorizationMiddleware(object):
    @run_only_once
    def resolve(self, next, root, info, **args):
        auth = info.context.headers.get("Authorization")

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

        return next(root, info, **args)
