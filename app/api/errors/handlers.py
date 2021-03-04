from flask import Blueprint
from flask_restplus import abort

from .errors import BadRequest


def add_error_handlers(bp: Blueprint) -> None:
    @bp.errorhandler(BadRequest)
    def handle_bad_request(error: BadRequest) -> None:
        payload = error.payload or {}
        abort(error.status, error.message, **payload)
