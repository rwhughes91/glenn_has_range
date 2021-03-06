from flask import Blueprint
from flask_restplus import Api

from .controllers import user_ns, playlist_ns, auth_ns
from .errors import add_error_handlers
from .graphql import graphql_endpoint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api = Api(
    api_blueprint,
    title="Glenn has range API",
    version="1.0",
    description="A RESTful Flask web service for Spotify playlists",
)

# Adding API routes
api.add_namespace(user_ns, path="/users")
api.add_namespace(playlist_ns, path="/playlists")
api.add_namespace(auth_ns)

# Adding Error Catching
add_error_handlers(api_blueprint)

# Adding graphql endpoint
api_blueprint.add_url_rule("/graphql", view_func=graphql_endpoint)
