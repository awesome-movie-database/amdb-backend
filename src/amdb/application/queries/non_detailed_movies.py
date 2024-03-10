from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetNonDetailedMoviesQuery:
    limit: int
    offset: int
