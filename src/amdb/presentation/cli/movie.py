from typing import Annotated

import typer

from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.commands.create_movie import CreateMovieCommand
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
    [green]Create[/green] a new movie.

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
