from dataclasses import dataclass

from amdb.domain.entities.base import Entity
from .user import UserId


@dataclass(slots=True)
class Profile(Entity):
    user_id: UserId
    achievements: int
    movie_ratings: int
    series_episodes_ratings: int
    movie_reviews: int
    series_reviews: int
    given_votes: int
    gained_votes: int