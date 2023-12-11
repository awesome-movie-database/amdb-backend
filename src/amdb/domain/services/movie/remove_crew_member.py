from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.person.person import Person


class RemoveMovieCrewMember(Service):
    def __call__(
        self,
        *,
        movie: Movie,
        crew_member_person: Person,
        timestamp: datetime,
    ) -> None:
        movie.updated_at = timestamp
        crew_member_person.updated_at = timestamp
