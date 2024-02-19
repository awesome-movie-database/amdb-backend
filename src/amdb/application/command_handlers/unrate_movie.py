from typing import cast

from amdb.domain.entities.movie import Movie
from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.unrate_movie import UnrateMovie
from amdb.application.common.gateways.permissions import (
    PermissionsGateway,
)
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.rating import RatingGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import (
    UNRATE_MOVIE_ACCESS_DENIED,
    USER_IS_NOT_OWNER,
    RATING_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.unrate_movie import UnrateMovieCommand


class UnrateMovieHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        unrate_movie: UnrateMovie,
        permissions_gateway: PermissionsGateway,
        movie_gateway: MovieGateway,
        rating_gateway: RatingGateway,
        unit_of_work: UnitOfWork,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._unrate_movie = unrate_movie
        self._permissions_gateway = permissions_gateway
        self._movie_gateway = movie_gateway
        self._rating_gateway = rating_gateway
        self._unit_of_work = unit_of_work
        self._identity_provider = identity_provider

    def execute(self, command: UnrateMovieCommand) -> None:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_unrate_movie()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(UNRATE_MOVIE_ACCESS_DENIED)

        rating = self._rating_gateway.with_id(command.rating_id)
        if not rating:
            raise ApplicationError(RATING_DOES_NOT_EXIST)

        current_user_id = self._identity_provider.get_user_id()
        if current_user_id != rating.user_id:
            raise ApplicationError(USER_IS_NOT_OWNER)

        movie = self._movie_gateway.with_id(rating.movie_id)
        movie = cast(Movie, movie)

        self._unrate_movie(
            movie=movie,
            rating=rating,
        )
        self._rating_gateway.delete(rating)
        self._movie_gateway.update(movie)

        self._unit_of_work.commit()
