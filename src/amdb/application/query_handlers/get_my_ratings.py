from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.permissions_gateway import (
    PermissionsGateway,
)
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.application.common.interfaces.identity_provider import (
    IdentityProvider,
)
from amdb.application.queries.get_my_ratings import (
    GetMyRatingsQuery,
    GetMyRatingsResult,
)
from amdb.application.common.constants.exceptions import (
    GET_MY_RATINGS_ACCESS_DENIED,
)
from amdb.application.common.exception import ApplicationError


class GetMyRatingsHandler:
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

    def execute(self, query: GetMyRatingsQuery) -> GetMyRatingsResult:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_get_rating()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(GET_MY_RATINGS_ACCESS_DENIED)

        current_user_id = self._identity_provider.get_user_id()

        ratings = self._rating_gateway.list_with_user_id(
            user_id=current_user_id,
            limit=query.limit,
            offset=query.offset,
        )
        get_my_ratings_result = GetMyRatingsResult(
            ratings=ratings,  # type: ignore
            rating_count=len(ratings),
        )

        return get_my_ratings_result
