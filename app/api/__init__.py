from flask import Blueprint
from flask_restplus import Api

from .controllers import user_ns
from .errors import add_error_handlers

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api = Api(
    api_blueprint,
    title="Glenn has range API",
    version="1.0",
    description="A RESTful Flask web service for Spotify playlists",
)

api.add_namespace(user_ns, path="/users")
add_error_handlers(api_blueprint)