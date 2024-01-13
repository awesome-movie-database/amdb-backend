from unittest.mock import Mock
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.rating import Rating
from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.rate_movie import RateMovie
from amdb.domain.constants.exceptions import INVALID_RATING_VALUE
from amdb.domain.exception import DomainError
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.commands.rate_movie import RateMovieCommand
from amdb.application.command_handlers.rate_movie import RateMovieHandler
from amdb.application.common.constants.exceptions import (
    RATE_MOVIE_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
    MOVIE_ALREADY_RATED,
)
from amdb.application.common.exception import ApplicationError


USER_ID = UserId(uuid4())


@pytest.fixture(scope="module")
def identity_provider_with_valid_permissions() -> IdentityProvider:
    identity_provider = Mock()
    identity_provider.get_user_id = Mock(
        return_value=USER_ID,
    )
    identity_provider.get_permissions = Mock(
        return_value=4,
    )

    return identity_provider


@pytest.fixture(scope="module")
def identity_provider_with_invalid_permissions() -> IdentityProvider:
    identity_provider = Mock()
    identity_provider.get_user_id = Mock(
        return_value=USER_ID,
    )
    identity_provider.get_permissions = Mock(
        return_value=2,
    )

    return identity_provider


def test_rate_movie(
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_valid_permissions: IdentityProvider,
):
    user = User(
        id=USER_ID,
        name="John Doe",
    )
    user_gateway.save(user)

    movie = Movie(
        id=MovieId(uuid4()),
        title="Matrix",
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    unit_of_work.commit()

    rate_movie_command = RateMovieCommand(
        movie_id=movie.id,
        rating=9,
    )
    rate_movie_handler = RateMovieHandler(
        access_concern=AccessConcern(),
        rate_movie=RateMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_valid_permissions,
    )

    rate_movie_handler.execute(rate_movie_command)


def test_rate_movie_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_invalid_permissions: IdentityProvider,
):
    rate_movie_command = RateMovieCommand(
        movie_id=MovieId(uuid4()),
        rating=9,
    )
    rate_movie_handler = RateMovieHandler(
        access_concern=AccessConcern(),
        rate_movie=RateMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_invalid_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        rate_movie_handler.execute(rate_movie_command)

    assert error.value.message == RATE_MOVIE_ACCESS_DENIED


def test_rate_movie_should_raise_error_when_movie_does_not_exist(
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_valid_permissions: IdentityProvider,
):
    rate_movie_command = RateMovieCommand(
        movie_id=MovieId(uuid4()),
        rating=9,
    )
    rate_movie_handler = RateMovieHandler(
        access_concern=AccessConcern(),
        rate_movie=RateMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_valid_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        rate_movie_handler.execute(rate_movie_command)

    assert error.value.message == MOVIE_DOES_NOT_EXIST


def test_rate_movie_should_raise_error_when_movie_already_rated(
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_valid_permissions: IdentityProvider,
):
    user = User(
        id=USER_ID,
        name="John Doe",
    )
    user_gateway.save(user)

    movie = Movie(
        id=MovieId(uuid4()),
        title="Matrix",
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    rating = Rating(
        movie_id=movie.id,
        user_id=user.id,
        value=10,
        created_at=datetime.now(timezone.utc),
    )
    rating_gateway.save(rating)

    unit_of_work.commit()

    rate_movie_command = RateMovieCommand(
        movie_id=movie.id,
        rating=9,
    )
    rate_movie_handler = RateMovieHandler(
        access_concern=AccessConcern(),
        rate_movie=RateMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_valid_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        rate_movie_handler.execute(rate_movie_command)

    assert error.value.message == MOVIE_ALREADY_RATED


@pytest.mark.parametrize("rating_value", (11, 0, 4.2))
def test_rate_movie_should_raise_error_when_rating_is_invalid(
    rating_value: float,
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_valid_permissions: IdentityProvider,
):
    user = User(
        id=USER_ID,
        name="John Doe",
    )
    user_gateway.save(user)

    movie = Movie(
        id=MovieId(uuid4()),
        title="Matrix",
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    unit_of_work.commit()

    rate_movie_command = RateMovieCommand(
        movie_id=movie.id,
        rating=rating_value,
    )
    rate_movie_handler = RateMovieHandler(
        access_concern=AccessConcern(),
        rate_movie=RateMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_valid_permissions,
    )

    with pytest.raises(DomainError) as error:
        rate_movie_handler.execute(rate_movie_command)

    assert error.value.message == INVALID_RATING_VALUE
