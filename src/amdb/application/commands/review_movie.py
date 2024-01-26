from dataclasses import dataclass

from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.review import ReviewType


@dataclass(frozen=True, slots=True)
class ReviewMovieCommand:
    movie_id: MovieId
    title: str
    content: str
    type: ReviewType
