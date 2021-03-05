from app.api.errors import BadRequest


class TestBadRequest:
    """Testing BadRequest exception"""

    def test_serialize_exception_payload(self) -> None:
        """It serializes the object into a dict with payload"""

        bad_request = BadRequest(
            "Example error", 400, {"error_message": "this is a message"}
        )

        serialized_request = bad_request.serialize()

        assert "message" in serialized_request
        assert "errors" in serialized_request

    def test_serialize_exception_no_payload(self) -> None:
        """It serializes the object into a dict without payload"""

        bad_request = BadRequest("Example error")

        serialized_request = bad_request.serialize()

        assert "message" in serialized_request
        assert "errors" not in serialized_request
