from uuid_extensions import uuid7

from amdb.domain.entities.movie import MovieId
from amdb.domain.services.create_movie import CreateMovie
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.commands.create_movie import CreateMovieCommand


class CreateMovieHandler:
    def __init__(
        self,
        *,
        create_movie: CreateMovie,
        movie_gateway: MovieGateway,
        unit_of_work: UnitOfWork,
        identity_provider: IdentityProvider,
    ) -> None:
        self._create_movie = create_movie
        self._movie_gateway = movie_gateway
        self._unit_of_work = unit_of_work
        self._identity_provider = identity_provider

    def execute(self, command: CreateMovieCommand) -> MovieId:
        movie = self._create_movie(
            id=MovieId(uuid7()),
            title=command.title,
            release_date=command.release_date,
        )
        self._movie_gateway.save(movie)

        self._unit_of_work.commit()

        return movie.id
