from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.favourites.favourites import Favourites
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.favourites.movie import FavouriteMovie


class AddMovieToFavourites(Service):
    def __call__(
        self,
        *,
        favourites: Favourites,
        movie: Movie,
        created_at: datetime,
    ) -> FavouriteMovie:
        favourites.updated_at = created_at

        return FavouriteMovie(
            favourites_id=favourites.id,
            movie_id=movie.id,
            created_at=created_at,
        )
