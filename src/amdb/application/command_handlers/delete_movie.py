from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.gateways.permissions import (
    PermissionsGateway,
)
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.rating import RatingGateway
from amdb.application.common.gateways.review import ReviewGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import (
    DELETE_MOVIE_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.delete_movie import DeleteMovieCommand


class DeleteMovieHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        permissions_gateway: PermissionsGateway,
        movie_gateway: MovieGateway,
        rating_gateway: RatingGateway,
        review_gateway: ReviewGateway,
        unit_of_work: UnitOfWork,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._permissions_gateway = permissions_gateway
        self._movie_gateway = movie_gateway
        self._rating_gateway = rating_gateway
        self._review_gateway = review_gateway
        self._unit_of_work = unit_of_work
        self._identity_provider = identity_provider

    def execute(self, command: DeleteMovieCommand) -> None:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_delete_movie()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(DELETE_MOVIE_ACCESS_DENIED)

        movie = self._movie_gateway.with_id(command.movie_id)
        if not movie:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        self._movie_gateway.delete(movie)
        self._rating_gateway.delete_with_movie_id(command.movie_id)
        self._review_gateway.delete_with_movie_id(command.movie_id)

        self._unit_of_work.commit()
