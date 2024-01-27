from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.review_gateway import ReviewGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import (
    GET_REVIEW_ACCESS_DENIED,
    REVIEW_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.queries.get_review import GetReviewQuery, GetReviewResult


class GetReviewHandler:
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

    def execute(self, query: GetReviewQuery) -> GetReviewResult:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_get_review()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(GET_REVIEW_ACCESS_DENIED)

        review = self._review_gateway.with_id(query.review_id)
        if not review:
            raise ApplicationError(REVIEW_DOES_NOT_EXIST)

        get_review_result = GetReviewResult(
            user_id=review.user_id,
            movie_id=review.movie_id,
            title=review.title,
            content=review.content,
            type=review.type,
            created_at=review.created_at,
        )

        return get_review_result
