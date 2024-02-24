from datetime import date

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.movie import MovieId, Movie
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.rating import RatingGateway
from amdb.application.common.gateways.review import ReviewGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.commands.delete_movie import DeleteMovieCommand
from amdb.application.command_handlers.delete_movie import DeleteMovieHandler
from amdb.application.common.constants.exceptions import MOVIE_DOES_NOT_EXIST
from amdb.application.common.exception import ApplicationError


def test_delete_movie(
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
):
    movie = Movie(
        id=MovieId(uuid7()),
        title="Matrix",
        release_date=date(1999, 3, 31),
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    unit_of_work.commit()

    delete_movie_command = DeleteMovieCommand(
        movie_id=movie.id,
    )
    delete_movie_handler = DeleteMovieHandler(
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        review_gateway=review_gateway,
        unit_of_work=unit_of_work,
    )

    delete_movie_handler.execute(delete_movie_command)


def test_delete_movie_should_raise_error_when_movie_does_not_exist(
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
):
    command = DeleteMovieCommand(
        movie_id=MovieId(uuid7()),
    )
    handler = DeleteMovieHandler(
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        review_gateway=review_gateway,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == MOVIE_DOES_NOT_EXIST
