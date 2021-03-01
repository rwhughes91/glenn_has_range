from typing import Dict, Any

from ..types import ErrorMessage


class StatusCodes:
    """Common status codes sent"""

    ok = 200
    bad = 400
    unauthorized = 401
    forbidden = 403
    not_found = 404
    error = 500


class BadRequest(Exception):
    """Custom exception class to be thrown when local error occurs"""

    def __init__(
        self, message: str, status: int = 400, payload: Dict[Any, Any] = None
    ) -> None:
        super(BadRequest, self).__init__(message)
        self.message = message
        self.status = status
        self.payload = payload

    def serialize(self) -> ErrorMessage:
        """Creates a JSON-compatible error message"""

        message: ErrorMessage = {"message": self.message}

        if self.payload:
            message["errors"] = self.payload

        return message
