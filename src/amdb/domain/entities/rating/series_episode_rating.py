from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.series.series import SeriesId
from amdb.domain.entities.user.user import UserId
from amdb.domain.value_objects import Rating


@dataclass(slots=True)
class SeriesEpisodeRating(Entity):
    series_id: SeriesId
    season_number: int
    episode_number: int
    user_id: UserId
    rating: Rating
    is_counted: bool
    created_at: datetime
