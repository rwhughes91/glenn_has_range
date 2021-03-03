import os
import json
import click
from coverage.cmdline import main
from flake8.main.cli import main as fmain

from app.api import api


def register(app) -> None:
    """Register cli commands for the app"""

    # Flask swagger
    @app.cli.command("swagger")
    def export_swagger() -> None:
        """Exports swagger schema to JSON file"""

        schema = api.__schema__
        with open("swagger.json", "w") as s:
            json.dump(schema, s, ensure_ascii=False, indent=2)

    # Flask test [CMD]
    @app.cli.group("test")
    def test() -> None:
        """Flask test cli group"""

        pass

    @test.command("run")
    def run() -> None:
        """Runs the unit tests of the app"""

        main(["run", "-m", "pytest", "--rootdir", "tests"])

    @test.command("report")
    def report() -> None:
        """Prints out the coverage report"""

        main(["report", "-m"])

    @test.command("html")
    def html() -> None:
        """Prints out the coverage report to HTML"""

        main(["html"])

    # Flask lint [CMD]
    @app.cli.group("lint")
    def lint() -> None:
        """Flask lint cli group"""

        pass

    @lint.command("flake8")
    def flake8() -> None:
        """Format application using flake8"""

        fmain(["--verbose", "app"])

    @lint.command("black")
    @click.option("--check/--no-check", default=False, help="Check what would change")
    def black(check: str) -> None:
        """Format application to match black style"""

        output = "black app"
        if check:
            output = "black --check app"

        os.system(output)

    @lint.command("mypy")
    def mypy():
        """Type checks the application with mypy"""

        os.system("mypy --config-file=tox.ini -p app")
