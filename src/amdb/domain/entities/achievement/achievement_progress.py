from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from amdb.domain.entities.base import Entity


@dataclass(slots=True)
class AchievementProgress(Entity):
    is_verified: Optional[bool]
    time_from_creating: Optional[timedelta]
    time_from_verification: Optional[timedelta]
    movie_ratings: Optional[int]
    series_episode_ratings: Optional[int]
    approved_reviews: Optional[int]
    movie_reviews: Optional[int]
    series_reviews: Optional[int]
    series_season_reviews: Optional[int]
    series_episode_reviews: Optional[int]
    given_votes: Optional[int]
    gained_votes: Optional[int]
