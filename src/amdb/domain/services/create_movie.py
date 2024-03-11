from datetime import date

from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.constants.exceptions import INVALID_MOVIE_TITLE
from amdb.domain.exception import DomainError


MOVIE_TITLE_MIN_LENGTH = 1
MOVIE_TITLE_MAX_LENGTH = 128


class CreateMovie:
    def __call__(
        self,
        *,
        id: MovieId,
        title: str,
        release_date: date,
    ) -> Movie:
        self._validate_title(title)

        return Movie(
            id=id,
            title=title,
            release_date=release_date,
            rating=0,
            rating_count=0,
        )

    def _validate_title(self, title: str) -> None:
        title_length = len(title)
        if (
            title_length < MOVIE_TITLE_MIN_LENGTH
            or title_length > MOVIE_TITLE_MAX_LENGTH
        ):
            raise DomainError(INVALID_MOVIE_TITLE)
