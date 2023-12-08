from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.custom_list.custom_list import CustomList
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.custom_list.movie import CustomListMovie


class AddMovieToCustomList(Service):
    def __call__(
        self,
        *,
        custom_list: CustomList,
        movie: Movie,
        created_at: datetime,
    ) -> CustomListMovie:
        custom_list.updated_at = created_at

        return CustomListMovie(
            custom_list_id=custom_list.id,
            movie_id=movie.id,
            created_at=created_at,
        )
