from typing import List
from flask import request
from flask_restplus import Resource

from ..models import PlaylistDto, Playlist
from ..services import get_playlists, save_new_playlist, get_playlist, put_playlist
from ..decorators import expect_jwt

api = PlaylistDto.api
_playlist = PlaylistDto.playlist


@api.route("/")
class PlaylistList(Resource):
    """Resource controller for Playlists"""

    @api.doc("list all playlists")
    @api.marshal_list_with(_playlist, envelope="playlists")
    @expect_jwt(api)
    def get(self) -> List[Playlist]:
        """List all playlists"""
        return get_playlists()

    @api.doc("create a new playlist")
    @api.response(201, "Playlist successfully created")
    @api.response(400, "Playlist already exists")
    @api.expect(_playlist, validate=True)
    @api.marshal_with(_playlist, code=201, envelope="user")
    @expect_jwt(api)
    def post(self) -> Playlist:
        """Creates a new Playlist"""

        data = request.json
        return save_new_playlist(data)


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
    def put(self, playlist_id: str) -> Playlist:
        """Edit or create a playlist by the identifier passed"""

        data = request.json
        return put_playlist(playlist_id, data)
