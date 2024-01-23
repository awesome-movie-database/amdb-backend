import typer

from .person import person_commands
from .movie import movie_commands
from .alembic import migration_commands


def setup_typer_command_handlers(app: typer.Typer) -> None:
    app.add_typer(person_commands)
    app.add_typer(movie_commands)
    app.add_typer(migration_commands)
