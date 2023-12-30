from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.unrate_movie import UnrateMovie
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import (
    MOVIE_DOES_NOT_EXIST,
    MOVIE_NOT_RATED,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.rate_movie import RateMovieCommand


class UnrateMovieHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        unrate_movie: UnrateMovie,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        rating_gateway: RatingGateway,
        unit_of_work: UnitOfWork,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._unrate_movie = unrate_movie
        self._user_gateway = user_gateway
        self._movie_gateway = movie_gateway
        self._rating_gateway = rating_gateway
        self._unit_of_work = unit_of_work
        self._identity_provider = identity_provider
    
    def execute(self, command: RateMovieCommand) -> None:
        current_user_id = self._identity_provider.get_user_id()

        movie = self._movie_gateway.with_id(command.movie_id)
        if not movie:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)
        
        rating = self._rating_gateway.with_user_id_and_movie_id(
            user_id=current_user_id,
            movie_id=movie.id,
        )
        if not rating:
            raise ApplicationError(MOVIE_NOT_RATED)
        
        self._unrate_movie(
            movie=movie,
            rating=rating,
        )
        self._rating_gateway.delete(rating)

        self._movie_gateway.update(movie)

        self._unit_of_work.commit()
