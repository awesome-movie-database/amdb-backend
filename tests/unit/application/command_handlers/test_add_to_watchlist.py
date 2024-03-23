from datetime import date, datetime, timezone
from unittest.mock import Mock

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import User, UserId
from amdb.domain.entities.movie import Movie, MovieId
from amdb.domain.entities.movie_for_later import MovieForLater, MovieForLaterId
from amdb.domain.services.watch_later import WatchLater
from amdb.domain.constants.exceptions import INVALID_MOVIE_FOR_LATER_NOTE
from amdb.domain.exception import DomainError
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.movie_for_later import (
    MovieForLaterGateway,
)
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.commands.add_to_watchlist import AddToWatchlistCommand
from amdb.application.command_handlers.add_to_watchlist import (
    AddToWatchlistHandler,
)
from amdb.application.common.constants.exceptions import (
    MOVIE_DOES_NOT_EXIST,
    MOVIE_ALREADY_IN_WATCHLIST,
)
from amdb.application.common.exception import ApplicationError


def test_add_to_watchlist(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    movie_for_later_gateway: MovieForLaterGateway,
    unit_of_work: UnitOfWork,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="john@doe.com",
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

    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id = Mock(return_value=user.id)

    command = AddToWatchlistCommand(
        movie_id=movie.id,
        note="Movie with Keanu Reeves that i saw on TV",
    )
    handler = AddToWatchlistHandler(
        watch_later=WatchLater(),
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        movie_for_later_gateway=movie_for_later_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider,
    )

    handler.execute(command)


def test_add_to_watchlist_should_raise_error_when_movie_does_not_exits(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    movie_for_later_gateway: MovieForLaterGateway,
    unit_of_work: UnitOfWork,
):
    identity_provider: IdentityProvider = Mock()

    command = AddToWatchlistCommand(
        movie_id=MovieId(uuid7()),
        note="Movie with Keanu Reeves that i saw on TV",
    )
    handler = AddToWatchlistHandler(
        watch_later=WatchLater(),
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        movie_for_later_gateway=movie_for_later_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == MOVIE_DOES_NOT_EXIST


def test_add_to_watchlist_should_raise_error_when_movie_already_in_watchlist(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    movie_for_later_gateway: MovieForLaterGateway,
    unit_of_work: UnitOfWork,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="john@doe.com",
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

    command = AddToWatchlistCommand(
        movie_id=movie.id,
        note="Movie with Keanu Reeves that i saw on TV",
    )
    handler = AddToWatchlistHandler(
        watch_later=WatchLater(),
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        movie_for_later_gateway=movie_for_later_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == MOVIE_ALREADY_IN_WATCHLIST


MOVIE_FOR_LATER_NOTE_LONGER_THAN_256_CHARACTERS = "_" * 257


def test_add_to_watchlist_should_raise_error_when_note_is_invalid(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    movie_for_later_gateway: MovieForLaterGateway,
    unit_of_work: UnitOfWork,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="john@doe.com",
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

    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id = Mock(return_value=user.id)

    command = AddToWatchlistCommand(
        movie_id=movie.id,
        note=MOVIE_FOR_LATER_NOTE_LONGER_THAN_256_CHARACTERS,
    )
    handler = AddToWatchlistHandler(
        watch_later=WatchLater(),
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        movie_for_later_gateway=movie_for_later_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider,
    )

    with pytest.raises(DomainError) as error:
        handler.execute(command)

    assert error.value.message == INVALID_MOVIE_FOR_LATER_NOTE
