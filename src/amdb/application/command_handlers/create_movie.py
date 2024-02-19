from uuid_extensions import uuid7

from amdb.domain.entities.movie import MovieId
from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.create_movie import CreateMovie
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import (
    CREATE_MOVIE_ACCESS_DENIED,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.create_movie import CreateMovieCommand


class CreateMovieHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        create_movie: CreateMovie,
        permissions_gateway: PermissionsGateway,
        movie_gateway: MovieGateway,
        unit_of_work: UnitOfWork,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._create_movie = create_movie
        self._permissions_gateway = permissions_gateway
        self._movie_gateway = movie_gateway
        self._unit_of_work = unit_of_work
        self._identity_provider = identity_provider

    def execute(self, command: CreateMovieCommand) -> MovieId:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_create_movie()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(CREATE_MOVIE_ACCESS_DENIED)

        movie = self._create_movie(
            id=MovieId(uuid7()),
            title=command.title,
            release_date=command.release_date,
        )
        self._movie_gateway.save(movie)

        self._unit_of_work.commit()

        return movie.id
