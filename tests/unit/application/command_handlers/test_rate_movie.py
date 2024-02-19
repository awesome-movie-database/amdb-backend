from unittest.mock import Mock
from datetime import date, datetime, timezone

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.rating import RatingId, Rating
from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.rate_movie import RateMovie
from amdb.domain.constants.exceptions import INVALID_RATING_VALUE
from amdb.domain.exception import DomainError
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.rating import RatingGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.commands.rate_movie import RateMovieCommand
from amdb.application.command_handlers.rate_movie import RateMovieHandler
from amdb.application.common.constants.exceptions import (
    RATE_MOVIE_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
    MOVIE_ALREADY_RATED,
)
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_rate_movie()
    identity_provider.get_permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_rate_movie(
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    user = User(
        id=UserId(uuid7()),
        name="John Doe",
    )
    user_gateway.save(user)

    movie = Movie(
        id=MovieId(uuid7()),
        title="Matrix",
        release_date=date(1999, 3, 31),
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.get_user_id = Mock(
        return_value=user.id,
    )

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
        identity_provider=identity_provider_with_correct_permissions,
    )

    rate_movie_handler.execute(rate_movie_command)


def test_rate_movie_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    rate_movie_command = RateMovieCommand(
        movie_id=MovieId(uuid7()),
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
        identity_provider=identity_provider_with_incorrect_permissions,
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
    identity_provider_with_correct_permissions: IdentityProvider,
):
    rate_movie_command = RateMovieCommand(
        movie_id=MovieId(uuid7()),
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
        identity_provider=identity_provider_with_correct_permissions,
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
    identity_provider_with_correct_permissions: IdentityProvider,
):
    user = User(
        id=UserId(uuid7()),
        name="John Doe",
    )
    user_gateway.save(user)

    movie = Movie(
        id=MovieId(uuid7()),
        title="Matrix",
        release_date=date(1999, 3, 31),
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    rating = Rating(
        id=RatingId(uuid7()),
        movie_id=movie.id,
        user_id=user.id,
        value=10,
        created_at=datetime.now(timezone.utc),
    )
    rating_gateway.save(rating)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.get_user_id = Mock(
        return_value=user.id,
    )

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
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        rate_movie_handler.execute(rate_movie_command)

    assert error.value.message == MOVIE_ALREADY_RATED


RATING_GREATER_THAN_10 = 11
RATING_LESS_THAN_A_HALF = 0
RATING_THAT_IS_NOT_DIVISABLE_BY_ONE_HALF = 4.2


@pytest.mark.parametrize(
    "rating_value",
    (
        RATING_GREATER_THAN_10,
        RATING_LESS_THAN_A_HALF,
        RATING_THAT_IS_NOT_DIVISABLE_BY_ONE_HALF,
    ),
)
def test_rate_movie_should_raise_error_when_rating_is_invalid(
    rating_value: float,
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    user = User(
        id=UserId(uuid7()),
        name="John Doe",
    )
    user_gateway.save(user)

    movie = Movie(
        id=MovieId(uuid7()),
        title="Matrix",
        release_date=date(1999, 3, 31),
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.get_user_id = Mock(
        return_value=user.id,
    )

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
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(DomainError) as error:
        rate_movie_handler.execute(rate_movie_command)

    assert error.value.message == INVALID_RATING_VALUE
