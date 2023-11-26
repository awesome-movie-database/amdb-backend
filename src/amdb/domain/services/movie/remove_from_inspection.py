from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.exceptions.movie import MovieNotUnderInspection


class RemoveMovieFromInspection(Service):

    def __call__(
        self,
        movie: Movie,
    ) -> None:
        if not movie.is_under_inspection:
            raise MovieNotUnderInspection()
        movie.is_under_inspection = False
        