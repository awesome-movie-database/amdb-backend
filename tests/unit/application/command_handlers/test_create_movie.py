from datetime import date

import pytest

from amdb.domain.services.create_movie import CreateMovie
from amdb.domain.constants.exceptions import INVALID_MOVIE_TITLE
from amdb.domain.exception import DomainError
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


MOVIE_TITLE_SHORTER_THAN_1_CHARACTER = ""
MOVIE_TITLE_LONGER_THAN_128_CHARACTERS = "_" * 129


@pytest.mark.parametrize(
    "movie_title",
    (
        MOVIE_TITLE_SHORTER_THAN_1_CHARACTER,
        MOVIE_TITLE_LONGER_THAN_128_CHARACTERS,
    ),
)
def test_create_movie_should_raise_error_when_title_is_invalid(
    movie_title: str,
    movie_gateway: MovieGateway,
    unit_of_work: UnitOfWork,
):
    command = CreateMovieCommand(
        title=movie_title,
        release_date=date(1999, 3, 31),
    )
    handler = CreateMovieHandler(
        create_movie=CreateMovie(),
        movie_gateway=movie_gateway,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(DomainError) as error:
        handler.execute(command)

    assert error.value.message == INVALID_MOVIE_TITLE
