from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.movie.movie import MovieId
from .custom_list import CustomListId


@dataclass(slots=True)
class CustomListMovie(Entity):
    custom_list_id: CustomListId
    movie_id: MovieId
    created_at: datetime
