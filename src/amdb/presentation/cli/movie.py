from datetime import datetime
from typing import Annotated
from uuid import UUID

import typer
import rich
import rich.box
import rich.table

from amdb.domain.entities.movie import MovieId
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.commands.create_movie import CreateMovieCommand
from amdb.application.commands.delete_movie import DeleteMovieCommand
from amdb.presentation.handler_factory import HandlerFactory


movie_commands = typer.Typer(name="movie")


@movie_commands.command()
def create(
    ctx: typer.Context,
    title: Annotated[str, typer.Option("--title", "-t", help="Movie title.")],
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
    ioc: HandlerFactory = ctx.obj["ioc"]
    identity_provider: IdentityProvider = ctx.obj["identity_provider"]

    with ioc.create_movie(identity_provider) as create_movie_handler:
        create_movie_command = CreateMovieCommand(
            title=title,
            release_date=release_date.date(),
        )
        movie_id = create_movie_handler.execute(create_movie_command)

    if not silently:
        rich.print(movie_id)


@movie_commands.command()
def delete(
    ctx: typer.Context,
    movie_id: Annotated[UUID, typer.Argument(help="Movie id.")],
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

    ioc: HandlerFactory = ctx.obj["ioc"]
    identity_provider: IdentityProvider = ctx.obj["identity_provider"]

    with ioc.delete_movie(identity_provider) as delete_movie_handler:
        delete_movie_command = DeleteMovieCommand(
            movie_id=MovieId(movie_id),
        )
        delete_movie_handler.execute(delete_movie_command)

    if not silently:
        rich.print(movie_id)
