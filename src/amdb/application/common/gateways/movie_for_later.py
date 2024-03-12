from typing import Protocol, Optional

from amdb.domain.entities.movie_for_later import MovieForLater, MovieForLaterId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.user import UserId


class MovieForLaterGateway(Protocol):
    def with_id(
        self,
        movie_for_later_id: MovieForLaterId,
    ) -> Optional[MovieForLater]:
        raise NotImplementedError

    def with_movie_id_and_user_id(
        self,
        user_id: UserId,
        movie_id: MovieId,
    ) -> Optional[MovieForLater]:
        raise NotImplementedError

    def save(self, movie_for_later: MovieForLater) -> None:
        raise NotImplementedError

    def delete(self, movie_for_later: MovieForLater) -> None:
        raise NotImplementedError
