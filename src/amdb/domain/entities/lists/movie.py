from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.movie.movie import MovieId
from .list import ListId


@dataclass(slots=True)
class ListMovie(Entity):
    list_id: ListId
    movie_id: MovieId
    created_at: datetime
