from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.lists.list import List
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.lists.movie import ListMovie


class AddMovieToList(Service):
    def __call__(
        self,
        *,
        list: List,
        movie: Movie,
        created_at: datetime,
    ) -> ListMovie:
        list.updated_at = created_at

        return ListMovie(
            list_id=list.id,
            movie_id=movie.id,
            created_at=created_at,
        )
