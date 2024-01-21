from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.queries.get_rating import GetRatingQuery, GetRatingResult
from amdb.application.common.constants.exceptions import (
    GET_RATING_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
    MOVIE_NOT_RATED,
)
from amdb.application.common.exception import ApplicationError


class GetRatingHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        permissions_gateway: PermissionsGateway,
        movie_gateway: MovieGateway,
        rating_gateway: RatingGateway,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._permissions_gateway = permissions_gateway
        self._movie_gateway = movie_gateway
        self._rating_gateway = rating_gateway
        self._identity_provider = identity_provider

    def execute(self, query: GetRatingQuery) -> GetRatingResult:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_get_rating()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(GET_RATING_ACCESS_DENIED)

        movie = self._movie_gateway.with_id(query.movie_id)
        if not movie:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        current_user_id = self._identity_provider.get_user_id()

        rating = self._rating_gateway.with_user_id_and_movie_id(
            user_id=current_user_id,
            movie_id=movie.id,
        )
        if not rating:
            raise ApplicationError(MOVIE_NOT_RATED)

        get_rating_result = GetRatingResult(
            value=rating.value,
            created_at=rating.created_at,
        )

        return get_rating_result
