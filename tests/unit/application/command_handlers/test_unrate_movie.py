from unittest.mock import Mock
from datetime import date, datetime, timezone

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.rating import RatingId, Rating
from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.unrate_movie import UnrateMovie
from amdb.application.common.interfaces.permissions_gateway import (
    PermissionsGateway,
)
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import (
    IdentityProvider,
)
from amdb.application.commands.unrate_movie import UnrateMovieCommand
from amdb.application.command_handlers.unrate_movie import UnrateMovieHandler
from amdb.application.common.constants.exceptions import (
    UNRATE_MOVIE_ACCESS_DENIED,
    USER_IS_NOT_OWNER,
    RATING_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_unrate_movie()
    identity_provider.get_permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_unrate_movie(
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
        value=9,
        created_at=datetime.now(timezone.utc),
    )
    rating_gateway.save(rating)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.get_user_id = Mock(
        return_value=user.id,
    )

    unrate_movie_command = UnrateMovieCommand(
        rating_id=rating.id,
    )
    unrate_movie_handler = UnrateMovieHandler(
        access_concern=AccessConcern(),
        unrate_movie=UnrateMovie(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_correct_permissions,
    )

    unrate_movie_handler.execute(unrate_movie_command)


def test_unrate_movie_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    unrate_movie_command = UnrateMovieCommand(
        rating_id=RatingId(uuid7()),
    )
    unrate_movie_handler = UnrateMovieHandler(
        access_concern=AccessConcern(),
        unrate_movie=UnrateMovie(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        unrate_movie_handler.execute(unrate_movie_command)

    assert error.value.message == UNRATE_MOVIE_ACCESS_DENIED


def test_unrate_movie_should_raise_error_when_rating_does_not_exist(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    unrate_movie_command = UnrateMovieCommand(
        rating_id=RatingId(uuid7()),
    )
    unrate_movie_handler = UnrateMovieHandler(
        access_concern=AccessConcern(),
        unrate_movie=UnrateMovie(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        unrate_movie_handler.execute(unrate_movie_command)

    assert error.value.message == RATING_DOES_NOT_EXIST


def test_unrate_movie_should_raise_error_when_user_is_not_rating_owner(
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
        value=9,
        created_at=datetime.now(timezone.utc),
    )
    rating_gateway.save(rating)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.get_user_id = Mock(
        return_value=UserId(uuid7()),
    )

    unrate_movie_command = UnrateMovieCommand(
        rating_id=rating.id,
    )
    unrate_movie_handler = UnrateMovieHandler(
        access_concern=AccessConcern(),
        unrate_movie=UnrateMovie(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        unrate_movie_handler.execute(unrate_movie_command)

    assert error.value.message == USER_IS_NOT_OWNER
