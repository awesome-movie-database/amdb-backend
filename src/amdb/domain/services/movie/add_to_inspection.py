from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.exceptions.movie import MovieUnderInspection


class AddMovieToInspection(Service):

    def __call__(
        self,
        movie: Movie,
    ) -> None:
        if movie.is_under_inspection:
            raise MovieUnderInspection()
        movie.is_under_inspection = True
        