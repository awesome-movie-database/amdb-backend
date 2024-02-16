from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.permissions_gateway import (
    PermissionsGateway,
)
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.identity_provider import (
    IdentityProvider,
)
from amdb.application.queries.get_movie import GetMovieQuery, GetMovieResult
from amdb.application.common.constants.exceptions import (
    GET_MOVIE_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


class GetMovieHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        permissions_gateway: PermissionsGateway,
        movie_gateway: MovieGateway,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._permissions_gateway = permissions_gateway
        self._movie_gateway = movie_gateway
        self._identity_provider = identity_provider

    def execute(self, query: GetMovieQuery) -> GetMovieResult:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_get_movie()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(GET_MOVIE_ACCESS_DENIED)

        movie = self._movie_gateway.with_id(query.movie_id)
        if not movie:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        get_movie_result = GetMovieResult(
            title=movie.title,
            release_date=movie.release_date,
            rating=movie.rating,
            rating_count=movie.rating_count,
        )

        return get_movie_result
