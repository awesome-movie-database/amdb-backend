from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.permissions_gateway import (
    PermissionsGateway,
)
from amdb.application.common.interfaces.review_gateway import ReviewGateway
from amdb.application.common.interfaces.identity_provider import (
    IdentityProvider,
)
from amdb.application.common.constants.exceptions import (
    GET_MY_REVIEWS_ACCESS_DENIED,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.queries.get_my_reviews import (
    GetMyReviewsQuery,
    GetMyReviewsResult,
)


class GetMyReviewsHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        permissions_gateway: PermissionsGateway,
        review_gateway: ReviewGateway,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._permissions_gateway = permissions_gateway
        self._review_gateway = review_gateway
        self._identity_provider = identity_provider

    def execute(self, query: GetMyReviewsQuery) -> GetMyReviewsResult:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_get_my_reviews()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(GET_MY_REVIEWS_ACCESS_DENIED)

        current_user_id = self._identity_provider.get_user_id()

        reviews = self._review_gateway.list_with_user_id(
            user_id=current_user_id,
            limit=query.limit,
            offset=query.offset,
        )
        get_my_reviews_result = GetMyReviewsResult(
            reviews=reviews,  # type: ignore
            review_count=len(reviews),
        )

        return get_my_reviews_result
