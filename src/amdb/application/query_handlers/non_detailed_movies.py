from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.readers.movie import MovieViewModelReader
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import GET_MOVIES_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError
from amdb.application.common.view_models.non_detailed_movie import NonDetailedMovieViewModel
from amdb.application.queries.non_detailed_movies import GetNonDetailedMoviesQuery


class GetNonDetailedMoviesHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        permissions_gateway: PermissionsGateway,
        movie_view_model_reader: MovieViewModelReader,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._permissions_gateway = permissions_gateway
        self._movie_view_model_reader = movie_view_model_reader
        self._identity_provider = identity_provider

    def execute(self, query: GetNonDetailedMoviesQuery) -> list[NonDetailedMovieViewModel]:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_get_movies()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(GET_MOVIES_ACCESS_DENIED)

        current_user_id = self._identity_provider.get_user_id()

        non_detailed_movie_models = self._movie_view_model_reader.list_non_detailed(
            current_user_id=current_user_id,
            limit=query.limit,
            offset=query.offset,
        )

        return non_detailed_movie_models
