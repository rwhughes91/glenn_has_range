from app import create_app, db
from app.api.models import Playlist, User

app = create_app("dev")


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Playlist": Playlist, "User": User}


if __name__ == "__main__":
    app.run(port=5000)
