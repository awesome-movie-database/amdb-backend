from datetime import datetime

from amdb.domain.entities.user import User
from amdb.domain.entities.movie import Movie
from amdb.domain.entities.movie_for_later import (
    MovieForLaterId,
    MovieForLater,
)
from amdb.domain.constants.exceptions import INVALID_MOVIE_FOR_LATER_NOTE
from amdb.domain.exception import DomainError


MOVIE_FOR_LATER_NOTE_MAX_LENGTH = 256


class WatchLater:
    def __call__(
        self,
        *,
        user: User,
        movie: Movie,
        id: MovieForLaterId,
        note: str,
        current_timestamp: datetime,
    ) -> MovieForLater:
        self._validate_note(note)

        return MovieForLater(
            id=id,
            user_id=user.id,
            movie_id=movie.id,
            note=note,
            created_at=current_timestamp,
        )

    def _validate_note(self, note: str) -> None:
        note_length = len(note)
        if note_length > MOVIE_FOR_LATER_NOTE_MAX_LENGTH:
            raise DomainError(INVALID_MOVIE_FOR_LATER_NOTE)
