from typing import Dict
from flask import request, g
from flask_restplus import Resource

from ..models import AuthDto
from ..services import login_user, logout_user
from ..decorators import expect_jwt

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route("/login")
class UserLogin(Resource):
    """User Login Resource"""

    @api.doc("user login")
    @api.response(200, "Successfully logged in")
    @api.response(401, "Email or password do not match")
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
    @api.response(200, "Successfully logged out")
    @expect_jwt(api, "Provide a valid auth token")
    def post(self) -> Dict[str, str]:
        """Logs a user out"""

        logout_user(g.token, g.payload)

        return {"message": "Successfully logged out"}
