from dataclasses import dataclass
from enum import IntEnum

from amdb.domain.entities.base import Entity
from amdb.domain.entities.person.person import PersonId
from .movie import MovieId


class MovieCrewMemberType(IntEnum):
    DIRECTOR = 0
    ART_DIRECTOR = 1
    CASTING_DIRECTOR = 2
    COMPOSER = 3
    OPERATOR = 4
    PRODUCER = 5
    EDITOR = 6
    SCREENWRITER = 7


@dataclass(slots=True)
class MovieCrewMember(Entity):
    movie_id: MovieId
    person_id: PersonId
    type: MovieCrewMemberType
