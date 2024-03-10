from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetMyDetailedRatingsQuery:
    limit: int
    offset: int
