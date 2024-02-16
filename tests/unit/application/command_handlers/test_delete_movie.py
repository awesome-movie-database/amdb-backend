from unittest.mock import Mock
from datetime import date

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.permissions_gateway import (
    PermissionsGateway,
)
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.application.common.interfaces.review_gateway import ReviewGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import (
    IdentityProvider,
)
from amdb.application.commands.delete_movie import DeleteMovieCommand
from amdb.application.command_handlers.delete_movie import DeleteMovieHandler
from amdb.application.common.constants.exceptions import (
    DELETE_MOVIE_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_delete_movie()
    identity_provider.get_permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_delete_movie(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
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
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        review_gateway=review_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_correct_permissions,
    )

    delete_movie_handler.execute(delete_movie_command)


def test_delete_movie_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    delete_movie_command = DeleteMovieCommand(
        movie_id=MovieId(uuid7()),
    )
    delete_movie_handler = DeleteMovieHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        review_gateway=review_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        delete_movie_handler.execute(delete_movie_command)

    assert error.value.message == DELETE_MOVIE_ACCESS_DENIED


def test_delete_movie_should_raise_error_when_movie_does_not_exist(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    delete_movie_command = DeleteMovieCommand(
        movie_id=MovieId(uuid7()),
    )
    delete_movie_handler = DeleteMovieHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        review_gateway=review_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        delete_movie_handler.execute(delete_movie_command)

    assert error.value.message == MOVIE_DOES_NOT_EXIST
