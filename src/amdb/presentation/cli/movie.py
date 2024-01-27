from datetime import datetime
from typing import Annotated
from uuid import UUID

import typer
import rich
import rich.box
import rich.table

from amdb.domain.entities.movie import MovieId
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.commands.create_movie import CreateMovieCommand
from amdb.application.commands.delete_movie import DeleteMovieCommand
from amdb.application.queries.get_movies import GetMoviesQuery
from amdb.application.queries.get_movie import GetMovieQuery
from amdb.presentation.handler_factory import HandlerFactory


movie_commands = typer.Typer(name="movie")


@movie_commands.command()
def list(
    ctx: typer.Context,
    limit: Annotated[
        int,
        typer.Option(
            "--limit",
            "-l",
            help="Number of movies that should be [blue]listed[/blue].",
            max=200,
            min=1,
        ),
    ] = 100,
    offset: Annotated[
        int,
        typer.Option(
            "--offset",
            "-o",
            help="Number of movies that should be offsetted.",
            min=0,
        ),
    ] = 0,
) -> None:
    """
    [blue]List[/blue] movies.
    """
    ioc: HandlerFactory = ctx.obj["ioc"]
    identity_provider: IdentityProvider = ctx.obj["identity_provider"]

    with ioc.get_movies(identity_provider) as get_movies_handler:
        get_movies_query = GetMoviesQuery(
            limit=limit,
            offset=offset,
        )
        get_movies_result = get_movies_handler.execute(get_movies_query)

    movies_table = rich.table.Table(
        "id",
        "title",
        "release_date",
        "rating",
        "rating_count",
        box=rich.box.ROUNDED,
    )
    for movie in get_movies_result.movies:
        movies_table.add_row(
            str(movie.id),
            movie.title,
            str(movie.release_date),
            str(movie.rating),
            str(movie.rating_count),
        )

    rich.print(movies_table)
    rich.print(
        f"Listed movie count: {get_movies_result.movie_count}",
        f"with limit: {limit}",
        f"and offset: {offset}",
    )


@movie_commands.command()
def get(
    ctx: typer.Context,
    movie_id: Annotated[UUID, typer.Argument(help="Movie id.")],
) -> None:
    """
    [blue]Get[/blue] movie.
    """
    ioc: HandlerFactory = ctx.obj["ioc"]
    identity_provider: IdentityProvider = ctx.obj["identity_provider"]

    with ioc.get_movie(identity_provider) as get_movie_handler:
        get_movie_query = GetMovieQuery(
            movie_id=MovieId(movie_id),
        )
        get_movie_result = get_movie_handler.execute(get_movie_query)

    movies_table = rich.table.Table(
        "id",
        "title",
        "release_date",
        "rating",
        "rating_count",
        box=rich.box.ROUNDED,
    )
    movies_table.add_row(
        str(movie_id),
        get_movie_result.title,
        str(get_movie_result.release_date),
        str(get_movie_result.rating),
        str(get_movie_result.rating_count),
    )

    rich.print(movies_table)


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
