from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.readers.movie import MovieViewModelReader
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import (
    GET_MOVIE_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.common.view_models.detailed_movie import DetailedMovieViewModel
from amdb.application.queries.detailed_movie import GetDetailedMovieQuery


class GetDetailedMovieHandler:
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

    def execute(self, query: GetDetailedMovieQuery) -> DetailedMovieViewModel:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_get_movie()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(GET_MOVIE_ACCESS_DENIED)

        current_user_id = self._identity_provider.get_user_id()

        detailed_movie_view_model = self._movie_view_model_reader.detailed(
            movie_id=query.movie_id,
            current_user_id=current_user_id,
        )
        if not detailed_movie_view_model:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        return detailed_movie_view_model
