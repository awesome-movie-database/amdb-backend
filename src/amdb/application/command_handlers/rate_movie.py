from datetime import datetime, timezone
from typing import cast

from amdb.domain.entities.user import User
from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.rate_movie import RateMovie
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import (
    RATE_MOVIE_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
    MOVIE_ALREADY_RATED,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.rate_movie import RateMovieCommand


class RateMovieHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        rate_movie: RateMovie,
        permissions_gateway: PermissionsGateway,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        rating_gateway: RatingGateway,
        unit_of_work: UnitOfWork,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._rate_movie = rate_movie
        self._permissions_gateway = permissions_gateway
        self._user_gateway = user_gateway
        self._movie_gateway = movie_gateway
        self._rating_gateway = rating_gateway
        self._unit_of_work = unit_of_work
        self._identity_provider = identity_provider

    def execute(self, command: RateMovieCommand) -> None:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_rate_movie()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(RATE_MOVIE_ACCESS_DENIED)

        movie = self._movie_gateway.with_id(command.movie_id)
        if not movie:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        current_user_id = self._identity_provider.get_user_id()

        rating = self._rating_gateway.with_user_id_and_movie_id(
            user_id=current_user_id,
            movie_id=movie.id,
        )
        if rating:
            raise ApplicationError(MOVIE_ALREADY_RATED)

        user = self._user_gateway.with_id(current_user_id)
        user = cast(User, user)

        new_rating = self._rate_movie(
            user=user,
            movie=movie,
            rating=command.rating,
            current_timestamp=datetime.now(timezone.utc),
        )
        self._rating_gateway.save(new_rating)
        self._movie_gateway.update(movie)

        self._unit_of_work.commit()
