import json
from app import create_app, db
from app.api import api
from app.api.models import Playlist, User, BlacklistToken

app = create_app("dev")
app.app_context().push()


@app.cli.command("swagger")
def export_swagger():
    schema = api.__schema__
    with open("swagger.json", "w") as s:
        json.dump(schema, s, ensure_ascii=False, indent=2)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "api": api,
        "Playlist": Playlist,
        "User": User,
        "BlacklistToken": BlacklistToken,
    }


if __name__ == "__main__":
    app.run(port=5000)
