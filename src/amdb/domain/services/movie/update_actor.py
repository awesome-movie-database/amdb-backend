from datetime import datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.movie.actor import MovieActor
from amdb.domain.constants import Unset, unset


class UpdateMovieActor(Service):
    def __call__(
        self,
        *,
        actor: MovieActor,
        movie: Movie,
        person: Person,
        timestamp: datetime,
        role: Union[str, None, Unset] = unset,
        is_star: Union[bool, None, Unset] = unset,
    ) -> None:
        movie.updated_at = timestamp
        person.updated_at = timestamp

        self._update_entity(
            entity=actor,
            role=role,
            is_star=is_star,
        )
