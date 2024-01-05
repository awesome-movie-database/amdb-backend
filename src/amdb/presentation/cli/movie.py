from typing import Annotated
from uuid import UUID

import typer

from amdb.domain.entities.movie import MovieId
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.commands.create_movie import CreateMovieCommand
from amdb.application.commands.delete_movie import DeleteMovieCommand
from amdb.presentation.handler_factory import HandlerFactory


movie_command = typer.Typer(name="movie")


@movie_command.command()
def create(
    ctx: typer.Context,
    title: Annotated[
        str,
        typer.Argument(
            help="Title that will be used to [green]create[/green] movie.",
        ),
    ],
    silently: Annotated[
        bool,
        typer.Option(
            help="[green]Create[/green] movie without printing any information.",
        ),
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
        )
        movie_id = create_movie_handler.execute(
            command=create_movie_command,
        )

    if not silently:
        print(movie_id)


@movie_command.command()
def delete(
    ctx: typer.Context,
    movie_id: Annotated[
        UUID,
        typer.Argument(
            help="Movie id that will be used to [red]delete[/red] movie.",
        ),
    ],
    force: Annotated[
        bool,
        typer.Option(
            help="[red]Delete[/red] movie without confirmation.",
        ),
    ] = False,
    silently: Annotated[
        bool,
        typer.Option(
            help="[red]Delete[/red] movie without printing any information.",
        ),
    ] = False,
) -> None:
    """
    [red]Delete[/red] movie.

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
        delete_movie_handler = delete_movie_handler.execute(
            command=delete_movie_command,
        )

    if not silently:
        print(movie_id)
