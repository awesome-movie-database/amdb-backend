from datetime import date, datetime, timezone
from unittest.mock import Mock

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import User, UserId
from amdb.domain.entities.movie import Movie, MovieId
from amdb.domain.entities.movie_for_later import MovieForLater, MovieForLaterId
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.movie_for_later import (
    MovieForLaterGateway,
)
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.commands.delete_from_watchlist import (
    DeleteFromWatchlistCommand,
)
from amdb.application.command_handlers.delete_from_watchlist import (
    DeleteFromWatchlistHandler,
)
from amdb.application.common.constants.exceptions import (
    USER_IS_NOT_OWNER,
    MOVIE_NOT_IN_WATCHLIST,
)
from amdb.application.common.exception import ApplicationError


def test_delete_from_watchlist(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    movie_for_later_gateway: MovieForLaterGateway,
    unit_of_work: UnitOfWork,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="john@doe.com",
        telegram=None,
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

    movie_for_later = MovieForLater(
        id=MovieForLaterId(uuid7()),
        user_id=user.id,
        movie_id=movie.id,
        note="Movie with Keanu Reeves that i saw on TV",
        created_at=datetime.now(timezone.utc),
    )
    movie_for_later_gateway.save(movie_for_later)

    unit_of_work.commit()

    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id = Mock(return_value=user.id)

    command = DeleteFromWatchlistCommand(
        movie_for_later_id=movie_for_later.id,
    )
    handler = DeleteFromWatchlistHandler(
        movie_for_later_gateway=movie_for_later_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider,
    )

    handler.execute(command)


def test_delete_from_watchlist_should_raise_error_when_movie_not_in_watchlist(
    user_gateway: UserGateway,
    movie_for_later_gateway: MovieForLaterGateway,
    unit_of_work: UnitOfWork,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="john@doe.com",
        telegram=None,
    )
    user_gateway.save(user)

    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id = Mock(return_value=user.id)

    command = DeleteFromWatchlistCommand(
        movie_for_later_id=MovieForLaterId(uuid7()),
    )
    handler = DeleteFromWatchlistHandler(
        movie_for_later_gateway=movie_for_later_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == MOVIE_NOT_IN_WATCHLIST


def test_delete_from_watchlist_should_raise_error_when_user_is_not_owner(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    movie_for_later_gateway: MovieForLaterGateway,
    unit_of_work: UnitOfWork,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="john@doe.com",
        telegram=None,
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

    movie_for_later = MovieForLater(
        id=MovieForLaterId(uuid7()),
        user_id=user.id,
        movie_id=movie.id,
        note="Movie with Keanu Reeves that i saw on TV",
        created_at=datetime.now(timezone.utc),
    )
    movie_for_later_gateway.save(movie_for_later)

    unit_of_work.commit()

    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id = Mock(return_value=UserId(uuid7()))

    command = DeleteFromWatchlistCommand(
        movie_for_later_id=movie_for_later.id,
    )
    handler = DeleteFromWatchlistHandler(
        movie_for_later_gateway=movie_for_later_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == USER_IS_NOT_OWNER
