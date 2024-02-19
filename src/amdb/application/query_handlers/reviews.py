from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.readers.review import ReviewViewModelReader
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.view_models.review import ReviewViewModel
from amdb.application.common.constants.exceptions import (
    GET_REVIEWS_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.queries.reviews import GetReviewsQuery


class GetReviewsHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        permissions_gateway: PermissionsGateway,
        movie_gateway: MovieGateway,
        review_view_model_reader: ReviewViewModelReader,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._permissions_gateway = permissions_gateway
        self._movie_gateway = movie_gateway
        self._review_view_model_reader = review_view_model_reader
        self._identity_provider = identity_provider

    def execute(self, query: GetReviewsQuery) -> list[ReviewViewModel]:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_get_reviews()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(GET_REVIEWS_ACCESS_DENIED)

        movie = self._movie_gateway.with_id(query.movie_id)
        if not movie:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        review_view_models = self._review_view_model_reader.list(
            movie_id=query.movie_id,
            limit=query.limit,
            offset=query.offset,
        )

        return review_view_models
