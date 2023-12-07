from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.movie.movie import MovieId
from .favourites import FavouritesId


@dataclass(slots=True)
class FavouriteMovie(Entity):
    favourites_id: FavouritesId
    movie_id: MovieId
    created_at: datetime
