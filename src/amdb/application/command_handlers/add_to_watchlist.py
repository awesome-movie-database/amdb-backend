from datetime import datetime, timezone
from typing import cast

from uuid_extensions import uuid7

from amdb.domain.entities.user import User
from amdb.domain.entities.movie_for_later import MovieForLaterId
from amdb.domain.services.watch_later import WatchLater
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.movie_for_later import (
    MovieForLaterGateway,
)
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import (
    MOVIE_DOES_NOT_EXIST,
    MOVIE_ALREADY_IN_WATCHLIST,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.add_to_watchlist import AddToWatchlistCommand


class AddToWatchlistHandler:
    def __init__(
        self,
        *,
        watch_later: WatchLater,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        movie_for_later_gateway: MovieForLaterGateway,
        unit_of_work: UnitOfWork,
        identity_provider: IdentityProvider,
    ) -> None:
        self._watch_later = watch_later
        self._user_gateway = user_gateway
        self._movie_gateway = movie_gateway
        self._movie_for_later_gateway = movie_for_later_gateway
        self._unit_of_work = unit_of_work
        self._identity_provider = identity_provider

    def execute(self, command: AddToWatchlistCommand) -> MovieForLaterId:
        current_user_id = self._identity_provider.user_id()

        movie = self._movie_gateway.with_id(command.movie_id)
        if not movie:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        movie_for_later = (
            self._movie_for_later_gateway.with_movie_id_and_user_id(
                user_id=current_user_id,
                movie_id=command.movie_id,
            )
        )
        if movie_for_later:
            raise ApplicationError(MOVIE_ALREADY_IN_WATCHLIST)

        user = self._user_gateway.with_id(current_user_id)
        user = cast(User, user)

        new_movie_for_later = self._watch_later(
            id=MovieForLaterId(uuid7()),
            user=user,
            movie=movie,
            note=command.note,
            current_timestamp=datetime.now(timezone.utc),
        )
        self._movie_for_later_gateway.save(new_movie_for_later)

        return new_movie_for_later.id
