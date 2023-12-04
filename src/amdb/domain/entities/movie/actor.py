from dataclasses import dataclass
from typing import Optional

from amdb.domain.entities.base import Entity
from amdb.domain.entities.person.person import PersonId
from .movie import MovieId


@dataclass(slots=True)
class MovieActor(Entity):
    movie_id: MovieId
    person_id: PersonId

    role: Optional[str]
    is_star: Optional[bool]
