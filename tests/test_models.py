import uuid
from datetime import datetime
import jwt

from app.api.models import User, BlacklistToken
from config import key


class TestUserModel:
    """Testing user model"""

    user = User(
        public_id=str(uuid.uuid4()),
        email="fakeEmail.com",
        username="fakeUsername",
        password="fakePassword",
        registered_on=datetime.utcnow(),
    )

    def test_set_password(self) -> None:
        """It sets a hashed password on the object when the password is set"""

        assert self.user.password_hash is not None
        assert self.user.password_hash != "fakePassword"

    def test_check_password(self) -> None:
        """It confirms the hashed password matches the passed password"""

        assert self.user.check_password("anotherPassword") is False
        assert self.user.check_password("fakePassword") is True

    def test_encode_auth_token(self, db) -> None:
        """It encodes a JWT token with the user_id claim"""

        user = User.query.first()
        token = user.encode_auth_token(user.user_id)
        payload = jwt.decode(token, key or "", algorithms="HS256")

        assert payload["sub"] == user.user_id

    def test_decode_auth_token(self, db) -> None:
        """It decodes the JWT token and returns the user_id claim"""

        user = User.query.first()
        token = user.encode_auth_token(user.user_id)
        payload = user.decode_auth_token(token)

        assert payload == user.user_id


class TestBlacklistToken:
    """Testing blacklist model"""

    blacklist_token = BlacklistToken("token")

    def test_new_blacklist_token(self) -> None:
        """It sets the token and blacklisted_on fields during init"""

        assert self.blacklist_token.token == "token"
        assert self.blacklist_token.blacklisted_on is not None

    def test_check_blacklist(self, db) -> None:
        """It checks if the provided token has been blacklisted"""

        token = "token"
        assert BlacklistToken.check_blacklist(token) is False

        db.session.add(self.blacklist_token)
        db.session.commit()

        assert BlacklistToken.check_blacklist(token) is True
