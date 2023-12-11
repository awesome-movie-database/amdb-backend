from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.movie.crew_member import MovieCrewMemberType, MovieCrewMember


class CreateMovieCrewMember(Service):
    def __call__(
        self,
        *,
        movie: Movie,
        person: Person,
        type: MovieCrewMemberType,
        timestamp: datetime,
    ) -> MovieCrewMember:
        movie.updated_at = timestamp
        person.updated_at = timestamp

        return MovieCrewMember(
            movie_id=movie.id,
            person_id=person.id,
            type=type,
        )
