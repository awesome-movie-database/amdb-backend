from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.permissions_gateway import (
    PermissionsGateway,
)
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.application.common.interfaces.identity_provider import (
    IdentityProvider,
)
from amdb.application.queries.get_rating import GetRatingQuery, GetRatingResult
from amdb.application.common.constants.exceptions import (
    GET_RATING_ACCESS_DENIED,
    RATING_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


class GetRatingHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        permissions_gateway: PermissionsGateway,
        rating_gateway: RatingGateway,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._permissions_gateway = permissions_gateway
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

        rating = self._rating_gateway.with_id(query.rating_id)
        if not rating:
            raise ApplicationError(RATING_DOES_NOT_EXIST)

        get_rating_result = GetRatingResult(
            user_id=rating.user_id,
            movie_id=rating.movie_id,
            value=rating.value,
            created_at=rating.created_at,
        )

        return get_rating_result
