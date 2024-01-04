import typer

from .movie import movie_command
from .migration import migration_command


def setup_typer_command_handlers(app: typer.Typer) -> None:
    app.add_typer(movie_command)
    app.add_typer(migration_command)
