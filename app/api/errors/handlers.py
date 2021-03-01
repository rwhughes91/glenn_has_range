from flask import Blueprint


from .errors import BadRequest
from ..types import ErrorMessage


def add_error_handlers(bp: Blueprint) -> None:
    @bp.errorhandler(BadRequest)
    def handle_bad_request(error: BadRequest) -> ErrorMessage:
        return error.serialize()
