from datetime import date

from amdb.domain.services.create_movie import CreateMovie
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.commands.create_movie import CreateMovieCommand
from amdb.application.command_handlers.create_movie import CreateMovieHandler


def test_create_movie(
    movie_gateway: MovieGateway,
    unit_of_work: UnitOfWork,
):
    command = CreateMovieCommand(
        title="Matrix",
        release_date=date(1999, 3, 31),
    )
    handler = CreateMovieHandler(
        create_movie=CreateMovie(),
        movie_gateway=movie_gateway,
        unit_of_work=unit_of_work,
    )

    handler.execute(command)
