from dataclasses import dataclass

from amdb.domain.entities.movie import MovieId


@dataclass(frozen=True, slots=True)
class GetDetailedReviewsQuery:
    movie_id: MovieId
    limit: int
    offset: int
