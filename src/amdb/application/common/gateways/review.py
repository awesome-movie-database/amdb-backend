from typing import Optional, Protocol

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.review import ReviewId, Review


class ReviewGateway(Protocol):
    def with_id(self, review_id: ReviewId) -> Optional[Review]:
        raise NotImplementedError

    def with_movie_id_and_user_id(
        self,
        user_id: UserId,
        movie_id: MovieId,
    ) -> Optional[Review]:
        raise NotImplementedError

    def save(self, review: Review) -> None:
        raise NotImplementedError

    def delete_with_movie_id(self, movie_id: MovieId) -> None:
        raise NotImplementedError
