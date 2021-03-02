import json
import pytest
from app import create_app, db
from app.api import api
from app.api.models import Playlist, User, BlacklistToken

app = create_app("dev")
app.app_context().push()


@app.cli.command("swagger")
def export_swagger():
    """Exports swagger schema to JSON file"""

    schema = api.__schema__
    with open("swagger.json", "w") as s:
        json.dump(schema, s, ensure_ascii=False, indent=2)


@app.cli.command("test")
def test():
    """Runs the unit tests of the app"""

    pytest.main(["--rootdir", "./app/tests"])


@app.shell_context_processor
def make_shell_context():
    """Makes object available during shell"""

    return {
        "db": db,
        "api": api,
        "Playlist": Playlist,
        "User": User,
        "BlacklistToken": BlacklistToken,
    }


if __name__ == "__main__":
    app.run(port=5000)
