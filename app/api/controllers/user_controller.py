from typing import List
from flask import request
from flask_restplus import Resource

from ..models import UserDto, User
from ..services import get_users, save_new_user, get_user
from ..decorators import expect_jwt

api = UserDto.api
_user = UserDto.user


@api.route("/")
class UserList(Resource):
    """Resource controller for Users"""

    @api.doc("list all users")
    @api.marshal_list_with(_user, envelope="users")
    @expect_jwt(api)
    def get(self) -> List[User]:
        """List all registered users"""

        return get_users()

    @api.doc("create a new user")
    @api.response(201, "User successfully created")
    @api.response(400, "User already exists")
    @api.expect(_user, validate=True)
    @api.marshal_with(_user, code=201, envelope="user")
    @expect_jwt(api)
    def post(self) -> User:
        """Creates a new User"""

        data = request.json
        return save_new_user(data)


@api.route("/<string:public_id>")
@api.param("public_id", "The User identifier")
@api.response(404, "User not found")
class User(Resource):
    """Resource controller for a User"""

    @api.doc("get a user")
    @api.marshal_with(_user, envelope="user")
    @expect_jwt(api)
    def get(self, public_id: str) -> User:
        """Get a user by the identifier passed"""

        return get_user(public_id)
