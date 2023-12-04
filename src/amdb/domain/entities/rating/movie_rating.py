from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.movie.movie import MovieId
from amdb.domain.entities.user.user import UserId
from amdb.domain.value_objects import Rating


@dataclass(slots=True)
class MovieRating(Entity):
    movie_id: MovieId
    user_id: UserId
    rating: Rating
    created_at: datetime


class UncountedMovieRating(MovieRating):
    ...
