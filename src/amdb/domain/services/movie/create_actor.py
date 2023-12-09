from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.movie.actor import MovieActor


class CreateMovieActor(Service):
    def __call__(
        self,
        *,
        movie: Movie,
        person: Person,
        timestamp: datetime,
        role: Optional[str] = None,
        is_star: Optional[bool] = None,
    ) -> MovieActor:
        movie.updated_at = timestamp
        person.updated_at = timestamp

        return MovieActor(
            movie_id=movie.id,
            person_id=person.id,
            role=role,
            is_star=is_star,
        )
