from typing import Dict
from flask import request
from flask_restplus import Resource

from ..models import AuthDto
from ..services import login_user, logout_user

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route("/login")
class UserLogin(Resource):
    """User Login Resource"""

    @api.doc("user login")
    @api.expect(user_auth, validate=True)
    def post(self) -> Dict[str, str]:
        """Logs a user in"""

        post_data = request.json
        token = login_user(post_data)

        return {"message": "Successfully logged in", "Authorization": token}


@api.route("/logout")
class LogoutAPI(Resource):
    """Logout Resource"""

    @api.doc("logout a user")
    def post(self) -> Dict[str, str]:
        """Logs a user out"""

        auth_header = request.headers.get("Authorization")
        logout_user(auth_header)

        return {"message": "Successfully logged out"}
