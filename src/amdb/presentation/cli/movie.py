from datetime import datetime
from typing import Annotated
from uuid import UUID

import typer
import rich
from dishka import Container

from amdb.domain.entities.movie import MovieId
from amdb.application.commands.create_movie import CreateMovieCommand
from amdb.application.commands.delete_movie import DeleteMovieCommand
from amdb.application.command_handlers.create_movie import CreateMovieHandler
from amdb.application.command_handlers.delete_movie import DeleteMovieHandler


movie_commands = typer.Typer(
    name="movie",
    help="[yellow]Manage[/yellow] movies",
)


@movie_commands.command()
def create(
    ctx: typer.Context,
    title: Annotated[
        str,
        typer.Option("--title", "-t", help="Movie title."),
    ],
    release_date: Annotated[
        datetime,
        typer.Option("--release_date", "-rd", help="Movie release date."),
    ],
    silently: Annotated[
        bool,
        typer.Option("--silently", "-s", help="Do not print movie id."),
    ] = False,
) -> None:
    """
    [green]Create[/green] movie.

    If --silently is not used, will print movie id.
    """
    container: Container = ctx.obj["container"]

    with container() as request_container:
        handler = request_container.get(CreateMovieHandler)
        command = CreateMovieCommand(
            title=title,
            release_date=release_date,
        )
        movie_id = handler.execute(command)

    if not silently:
        rich.print(movie_id)


@movie_commands.command()
def delete(
    ctx: typer.Context,
    movie_id: Annotated[
        UUID,
        typer.Argument(help="Movie id."),
    ],
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Do not ask for confirmation."),
    ] = False,
    silently: Annotated[
        bool,
        typer.Option("--silently", "-s", help="Do not print movie id"),
    ] = False,
) -> None:
    """
    [red]Delete[/red] movie. Also [red]deletes[/red] ratings and
    reviews related to movie.

    If --force is not used, will ask for confirmation.
    If --silently is not used, will print movie id.
    """
    if not force:
        typer.confirm(
            text="Are you sure you want to delete movie?",
            default=True,
            abort=True,
        )

    container: Container = ctx.obj["container"]

    with container() as request_container:
        handler = request_container.get(DeleteMovieHandler)
        command = DeleteMovieCommand(movie_id=MovieId(movie_id))
        handler.execute(command)

    if not silently:
        rich.print(movie_id)
