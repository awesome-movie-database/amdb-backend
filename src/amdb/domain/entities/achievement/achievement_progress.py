from dataclasses import dataclass
from typing import Optional

from amdb.domain.entities.base import Entity


@dataclass(slots=True)
class AchievementProgress(Entity):
    movie_ratings: Optional[int]
    series_episode_ratings: Optional[int]
    approved_reviews: Optional[int]
    movie_reviews: Optional[int]
    series_reviews: Optional[int]
    series_season_reviews: Optional[int]
    series_episode_reviews: Optional[int]
    given_votes: Optional[int]
    gained_votes: Optional[int]
