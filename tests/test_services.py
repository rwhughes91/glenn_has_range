import pytest

from app.api.services import (
    save_token,
    login_user,
    logout_user,
    get_users,
    get_user,
    save_new_user,
    get_playlists,
    get_playlist,
    put_playlist,
    save_new_playlist,
)
from app.api.models import BlacklistToken
from app.api.errors import BadRequest


class TestAuthService:
    """Testing auth service"""

    def test_save_token_pass(self, db) -> None:
        """It saves the token to the blacklist table"""

        token = "my_token"
        res = save_token(token)

        assert res is True
        assert BlacklistToken.check_blacklist(token) is True

    def test_login_user_pass(self, db) -> None:
        """It finds the existing user by email and returns a JWT Token"""

        auth_data = {"email": "someEmail@google.com", "password": "testPasssword@123"}
        token = login_user(auth_data)

        assert token is not None

    def test_login_user_fail(self, db) -> None:
        """It raises an BadRequest exception when credentials don't match"""

        auth_data = {"email": "someEmail@google.com", "password": "wrongPassword@123"}
        with pytest.raises(BadRequest):
            login_user(auth_data)

    def test_logout_user(self, db) -> None:
        """It calls save_token if payload is an int or raises BadRequest"""

        token = "my_other_token"
        payload = 4

        res = logout_user(token, payload)

        assert res is True


class TestUserService:
    """Testing user service"""

    new_user = {
        "email": "newEmail@yahoo.com",
        "username": "testUser",
        "password": "newPasswordFake",
    }

    def test_get_users(self, db) -> None:
        """It returns all the registered users"""

        users = get_users()

        assert len(users) >= 1

    def test_get_user_pass(self, db) -> None:
        """It returns the user by public_id"""

        user = get_user("9a2a2576-1683-4cb4-aa15-10728dd83ac9")

        assert user is not None

    def test_get_user_fail(self, db) -> None:
        """It raises an exception if user doesn't exist"""

        with pytest.raises(BadRequest):
            get_user("fakeEmail@gmail.com")

    def test_save_new_user_pass(self, db) -> None:
        """It creates a new user"""

        user = save_new_user(self.new_user)

        assert user is not None

    def test_save_new_user_fail(self, db) -> None:
        """It raises a BadRequest if user already exists"""

        with pytest.raises(BadRequest):
            save_new_user(
                {
                    "email": "someEmail@google.com",
                    "username": "someEmail@google.com",
                    "password": "testPasssword@123",
                }
            )


class TestPlaylistService:
    """Testing playlist service"""

    new_playlist = {
        "datasource": "reddit",
        "screen_name": "new name",
        "playlist_link": "https://somelink12.com",
        "playlist_description": "This is a description",
    }

    def test_get_playlists(self, db) -> None:
        """It returns all the spotify playlists"""

        playlists = get_playlists()

        assert len(playlists) >= 3

    def test_get_playlist_pass(self, db) -> None:
        """It gets a spotify playlist by id"""

        playlist = get_playlist("a600f327-a53c-4d2d-8d31-41f5a8b81121")

        assert playlist is not None

    def test_get_playlist_fail(self, db) -> None:
        """It raises a BadRequest when id does not exist"""

        with pytest.raises(BadRequest):
            get_playlist("a600f327-a53c-4d2d-8d31-41f5a8b81122")

        with pytest.raises(BadRequest):
            get_playlist("12")

    def test_put_playlist_pass(self, db) -> None:
        """It adds or edits a spotify playlist by id"""

        playlist = put_playlist(
            "87569b1d-8975-4522-97a4-039346c53512", self.new_playlist
        )

        assert playlist is not None

    def test_put_playlist_fail(self, db) -> None:
        """It raises a BadRequest when id does not exist"""

        with pytest.raises(BadRequest):
            put_playlist("12", self.new_playlist)

    def test_save_new_playlist_pass(self, db) -> None:

        payload = self.new_playlist
        payload["playlist_link"] = "somelink"
        playlist = save_new_playlist(self.new_playlist)

        assert playlist is not None

    def test_save_new_playlist_fail(self, db) -> None:

        with pytest.raises(BadRequest):
            save_new_playlist(self.new_playlist)
