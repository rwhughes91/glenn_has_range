class TestPlaylistController:
    """Testing Playlists Controller"""

    path = "/api/playlists/"
    playlist_id = "87569b1d-8975-4522-97a4-039346c53512"

    def test_get_playlists_pass(self, client_request) -> None:
        """It returns all the saved spotify playlists"""

        res = client_request(self.path).json

        assert "playlists" in res
        assert len(res["playlists"]) >= 3

    def test_get_playlists_fail(self, client) -> None:
        """It tests this route is protected"""

        res = client.get(self.path)
        status_code = res.status_code

        assert status_code == 401

    def test_post_playlists_pass(self, client_request) -> None:
        """It creates a new playlist"""

        res = client_request(
            self.path,
            "post",
            {
                "datasource": "reddit",
                "screen_name": "name1",
                "playlist_link": "new link to playlist",
                "playlist_description": "First description",
            },
        ).json

        assert "playlist" in res
        assert res["playlist"]["playlist_link"] == "new link to playlist"

    def test_post_playlists_fail(self, client) -> None:
        """It tests this route is protected"""

        res = client.post(
            "api/playlists/",
            json={
                "datasource": "reddit",
                "screen_name": "name1",
                "playlist_link": "new link to playlist",
                "playlist_description": "First description",
            },
        )
        status_code = res.status_code

        assert status_code == 401

    def test_get_playlist_pass(self, client_request) -> None:
        """It returns a playlist by the passed id"""

        res = client_request(self.path + self.playlist_id).json

        assert "playlist" in res
        assert res["playlist"]["playlist_id"] == self.playlist_id

    def test_get_playlist_fail(self, client) -> None:
        """It tests this route is protected"""

        res = client.get(self.path + self.playlist_id)
        status_code = res.status_code

        assert status_code == 401

    def test_put_playlist_pass(self, client_request) -> None:
        """It edits a playlist passed id"""

        res = client_request(
            self.path + self.playlist_id,
            "put",
            {
                "datasource": "reddit",
                "screen_name": "name1",
                "playlist_link": "new edited link to playlist",
                "playlist_description": "First description",
            },
        ).json

        assert "playlist" in res
        assert res["playlist"]["playlist_id"] == self.playlist_id

    def test_put_playlist_fail(self, client) -> None:
        """It tests this route is protected"""

        res = client.put(
            "api/playlists/12",
            json={
                "datasource": "reddit",
                "screen_name": "name1",
                "playlist_link": "new edited link to playlist",
                "playlist_description": "First description",
            },
        )
        status_code = res.status_code

        assert status_code == 401


class TestUserController:
    """Testing user controller"""

    path = "/api/users/"
    user_id = "9a2a2576-1683-4cb4-aa15-10728dd83ac9"

    def test_get_users_pass(self, client_request) -> None:
        """It returns the registered users"""

        res = client_request(self.path).json

        assert "users" in res
        assert len(res["users"]) >= 1

    def test_get_users_fail(self, client) -> None:
        """It tests this route is protected"""

        res = client.get(self.path)
        status_code = res.status_code

        assert status_code == 401

    def test_get_user_pass(self, client_request) -> None:
        """It returns the registered user"""

        res = client_request(self.path + self.user_id).json

        assert "user" in res
        assert res["user"]["public_id"] == self.user_id

    def test_get_user_fail(self, client) -> None:
        """It tests this route is protected"""

        res = client.get(self.path + self.user_id)
        status_code = res.status_code

        assert status_code == 401


class TestAuthController:
    """Testing auth controller"""

    path = "/api/auth/"

    def test_logout(self, client_request) -> None:
        """It logs the user out"""

        res = client_request(self.path + "logout", "post")
        status_code = res.status_code

        assert status_code == 200
