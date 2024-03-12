from amdb.application.common.gateways.movie_for_later import (
    MovieForLaterGateway,
)
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import (
    USER_IS_NOT_OWNER,
    MOVIE_NOT_IN_WATCHLIST,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.delete_from_watchlist import (
    DeleteFromWatchlistCommand,
)


class DeleteFromWatchlistHandler:
    def __init__(
        self,
        *,
        movie_for_later_gateway: MovieForLaterGateway,
        unit_of_work: UnitOfWork,
        identity_provider: IdentityProvider,
    ) -> None:
        self._movie_for_later_gateway = movie_for_later_gateway
        self._unit_of_work = unit_of_work
        self._identity_provider = identity_provider

    def execute(self, command: DeleteFromWatchlistCommand) -> None:
        current_user_id = self._identity_provider.user_id()

        movie_for_later = self._movie_for_later_gateway.with_id(
            command.movie_for_later_id,
        )
        if not movie_for_later:
            raise ApplicationError(MOVIE_NOT_IN_WATCHLIST)

        if movie_for_later.user_id != current_user_id:
            raise ApplicationError(USER_IS_NOT_OWNER)

        self._movie_for_later_gateway.delete(movie_for_later)

        self._unit_of_work.commit()
