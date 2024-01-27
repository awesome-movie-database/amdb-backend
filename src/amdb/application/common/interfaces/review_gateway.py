from typing import Optional, Protocol

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.review import Review


class ReviewGateway(Protocol):
    def with_movie_id_and_user_id(
        self,
        user_id: UserId,
        movie_id: MovieId,
    ) -> Optional[Review]:
        raise NotImplementedError

    def list_with_movie_id(
        self,
        movie_id: MovieId,
        limit: int,
        offset: int,
    ) -> list[Review]:
        raise NotImplementedError

    def save(self, review: Review) -> None:
        raise NotImplementedError
