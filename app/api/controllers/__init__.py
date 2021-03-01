from .user_controller import api as user_ns
from .playlist_controller import api as playlist_ns
from .auth_controller import api as auth_ns

__all__ = ["user_ns", "playlist_ns", "auth_ns"]
