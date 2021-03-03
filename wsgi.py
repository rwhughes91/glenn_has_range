from typing import Dict, Any

from app import create_app, db, cli
from app.api import api
from app.api.models import Playlist, User, BlacklistToken

app = create_app("dev")
cli.register(app)
app.app_context().push()


@app.shell_context_processor
def make_shell_context() -> Dict[str, Any]:
    """Make objects available during shell"""

    return {
        "db": db,
        "api": api,
        "Playlist": Playlist,
        "User": User,
        "BlacklistToken": BlacklistToken,
    }


if __name__ == "__main__":
    app.run(port=5000)
