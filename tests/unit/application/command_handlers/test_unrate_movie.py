from unittest.mock import Mock
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.rating import Rating
from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.unrate_movie import UnrateMovie
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.commands.unrate_movie import UnrateMovieCommand
from amdb.application.command_handlers.unrate_movie import UnrateMovieHandler
from amdb.application.common.constants.exceptions import (
    UNRATE_MOVIE_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
    MOVIE_NOT_RATED,
)
from amdb.application.common.exception import ApplicationError


@pytest.fixture(scope="module")
def identity_provider_with_valid_permissions() -> IdentityProvider:
    identity_provider = Mock()
    identity_provider.get_permissions = Mock(
        return_value=4,
    )

    return identity_provider


@pytest.fixture(scope="module")
def identity_provider_with_invalid_permissions() -> IdentityProvider:
    identity_provider = Mock()
    identity_provider.get_permissions = Mock(
        return_value=2,
    )

    return identity_provider


def test_unrate_movie(
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_valid_permissions: IdentityProvider,
):
    user = User(
        id=UserId(uuid4()),
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
        value=9,
        created_at=datetime.now(timezone.utc),
    )
    rating_gateway.save(rating)

    unit_of_work.commit()

    unrate_movie_command = UnrateMovieCommand(
        movie_id=movie.id,
    )
    unrate_movie_handler = UnrateMovieHandler(
        access_concern=AccessConcern(),
        unrate_movie=UnrateMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_valid_permissions,
    )

    unrate_movie_handler.execute(
        command=unrate_movie_command,
    )


def test_unrate_movie_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_invalid_permissions: IdentityProvider,
):
    unrate_movie_command = UnrateMovieCommand(
        movie_id=MovieId(uuid4()),
    )
    unrate_movie_handler = UnrateMovieHandler(
        access_concern=AccessConcern(),
        unrate_movie=UnrateMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_invalid_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        unrate_movie_handler.execute(
            command=unrate_movie_command,
        )
    
    assert error.value.message == UNRATE_MOVIE_ACCESS_DENIED


def test_unrate_movie_should_raise_error_when_movie_does_not_exist(
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_valid_permissions: IdentityProvider,
):
    unrate_movie_command = UnrateMovieCommand(
        movie_id=MovieId(uuid4()),
    )
    unrate_movie_handler = UnrateMovieHandler(
        access_concern=AccessConcern(),
        unrate_movie=UnrateMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_valid_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        unrate_movie_handler.execute(
            command=unrate_movie_command,
        )
    
    assert error.value.message == MOVIE_DOES_NOT_EXIST


def test_unrate_movie_should_raise_error_when_movie_is_not_rated(
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_valid_permissions: IdentityProvider,
):
    user = User(
        id=UserId(uuid4()),
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

    unrate_movie_command = UnrateMovieCommand(
        movie_id=movie.id,
    )
    unrate_movie_handler = UnrateMovieHandler(
        access_concern=AccessConcern(),
        unrate_movie=UnrateMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_valid_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        unrate_movie_handler.execute(
            command=unrate_movie_command,
        )
    
    assert error.value.message == MOVIE_NOT_RATED
