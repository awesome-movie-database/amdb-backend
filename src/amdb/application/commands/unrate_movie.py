from dataclasses import dataclass

from amdb.domain.entities.rating import RatingId


@dataclass(frozen=True, slots=True)
class UnrateMovieCommand:
    rating_id: RatingId
