from typing import List
from flask import request, g
from flask_restplus import Resource

from ..models import PlaylistDto, Playlist
from ..services import get_playlists, save_new_playlist, get_playlist, put_playlist
from ..decorators import expect_jwt, admin

api = PlaylistDto.api
_playlist = PlaylistDto.playlist


@api.route("/")
class PlaylistList(Resource):
    """Resource controller for Playlists"""

    @api.doc(
        "list all playlists",
        params={
            "search": {
                "description": "full text search",
                "in": "query",
                "type": "string",
            },
            "datasource": {
                "description": "filter on datasource",
                "in": "query",
                "type": "string",
            },
            "screen_name": {
                "description": "filter on screen_name",
                "in": "query",
                "type": "string",
            },
            "playlist_link": {
                "description": "filter on playlist_link",
                "in": "query",
                "type": "string",
            },
            "playlist_description": {
                "description": "filter on description",
                "in": "query",
                "type": "string",
            },
            "skip": {
                "description": "number of items to skip",
                "in": "query",
                "type": "number",
            },
            "limit": {
                "description": "number of items to limit",
                "in": "query",
                "type": "number",
            },
        },
    )
    @api.marshal_list_with(_playlist, envelope="playlists")
    @expect_jwt(api)
    def get(self) -> List[Playlist]:
        """List all playlists"""

        filters_keys = [
            "datasource",
            "screen_name",
            "playlist_link",
            "playlist_description",
        ]
        filters = {
            key: request.args.get(key)
            for key in filters_keys
            if request.args.get(key) is not None
        }

        return get_playlists(
            search=request.args.get("search"),
            filters=filters,
            limit=request.args.get("limit"),
            skip=request.args.get("skip", 0),
        )

    @api.doc("create a new playlist")
    @api.response(201, "Playlist successfully created")
    @api.response(400, "Playlist already exists")
    @api.expect(_playlist, validate=True)
    @api.marshal_with(_playlist, code=201, envelope="playlist")
    @expect_jwt(api)
    @admin
    def post(self) -> Playlist:
        """Creates a new Playlist"""

        data = request.json
        return save_new_playlist(data, g.payload)


@api.route("/<string:playlist_id>")
@api.param("playlist_id", "The playlist identifier")
class Playlist(Resource):
    """Resource controller for a playlist"""

    @api.doc("get a playlist")
    @api.response(404, "Playlist not found")
    @api.marshal_with(_playlist, envelope="playlist")
    @expect_jwt(api)
    def get(self, playlist_id: str) -> Playlist:
        """Get a playlist by the identifier passed"""

        return get_playlist(playlist_id)

    @api.doc("edit a playlist")
    @api.response(200, "Playlist successfully edited")
    @api.response(201, "Playlist successfully created")
    @api.response(400, "Playlist_id must be a valid UUID")
    @api.expect(_playlist, validate=True)
    @api.marshal_with(_playlist, envelope="playlist")
    @expect_jwt(api)
    @admin
    def put(self, playlist_id: str) -> Playlist:
        """Edit or create a playlist by the identifier passed"""

        data = request.json
        return put_playlist(playlist_id, data, g.payload)
