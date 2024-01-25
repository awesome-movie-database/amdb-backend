from datetime import date

from amdb.domain.entities.movie import MovieId, Movie


class CreateMovie:
    def __call__(
        self,
        *,
        id: MovieId,
        title: str,
        release_date: date,
    ) -> Movie:
        return Movie(
            id=id,
            title=title,
            release_date=release_date,
            rating=0,
            rating_count=0,
        )
