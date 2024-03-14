from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetMyDeatiledWatchlistQuery:
    limit: int
    offset: int
