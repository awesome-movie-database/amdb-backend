from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.queries.get_movies import GetMoviesQuery, GetMoviesResult
from amdb.application.common.constants.exceptions import GET_MOVIES_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError


class GetMoviesHandler:
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

    def execute(self, query: GetMoviesQuery) -> GetMoviesResult:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_get_movies()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(GET_MOVIES_ACCESS_DENIED)

        movies = self._movie_gateway.list(
            limit=query.limit,
            offset=query.offset,
        )
        get_movies_result = GetMoviesResult(
            movies=movies,  # type: ignore
            movie_count=len(movies),
        )

        return get_movies_result
