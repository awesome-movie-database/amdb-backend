import typer

from .movie import movie_command


def setup_typer_command_handlers(app: typer.Typer) -> None:
    app.add_typer(movie_command)
