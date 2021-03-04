import os
import json
import sys
from coverage.cmdline import main
from flake8.main.cli import main as fmain

from app import create_app
from app.api import api


class ExportGroup:
    """Different exports available through CLI"""

    @staticmethod
    def swagger() -> None:
        """Exports swagger schema to JSON file"""

        app = create_app("dev")
        with app.app_context():
            schema = api.__schema__
            with open("swagger.json", "w") as s:
                json.dump(schema, s, ensure_ascii=False, indent=2)

    @staticmethod
    def postman() -> None:
        """Exports API as Postman collection"""

        app = create_app("dev")
        with app.app_context():
            collection = api.as_postman(urlvars=False, swagger=True)
            with open("postman.json", "w") as p:
                json.dump(collection, p, ensure_ascii=False, indent=2)

    @staticmethod
    def commands() -> None:
        print("Available commands: swagger and postman")


class TestGroup:
    """Different test options through CLI"""

    @staticmethod
    def run() -> None:
        """Runs the unit tests of the app"""

        main(["run", "-m", "pytest", "--rootdir", "tests"])

    @staticmethod
    def report() -> None:
        """Prints out the coverage report"""

        main(["report", "-m"])

    @staticmethod
    def html() -> None:
        """Prints out the coverage report to HTML"""

        main(["html"])

    @staticmethod
    def commands() -> None:
        print("Available commands: swagger and postman")


class LintGroup:
    """Different linting options through CLI"""

    @staticmethod
    def flake8() -> None:
        """Format application using flake8"""

        fmain(["app"])

    @staticmethod
    def black() -> None:
        """Format application to match black style"""

        os.system("black app")

    @staticmethod
    def mypy():
        """Type checks the application with mypy"""

        os.system("mypy --config-file=tox.ini -p app")

    @staticmethod
    def commands() -> None:
        print("Available commands: swagger and postman")


if __name__ == "__main__":
    groups = {"export": ExportGroup, "test": TestGroup, "lint": LintGroup}
    args = sys.argv[1:]

    if len(args) < 2:
        print("Not enough arguments. Example: python manage.py export swagger")

    elif not args[0] in groups:
        print(f"Available groups: {', '.join(groups.keys())}")

    else:
        group = groups[args[0]]

        # Get proper function to call based on CLI args
        command = getattr(group, args[1], None)

        if command:
            command()
        else:
            group.commands()
