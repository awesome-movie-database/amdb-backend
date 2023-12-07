from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.series.series import SeriesId
from .favourites import FavouritesId


@dataclass(slots=True)
class FavouriteSeries(Entity):
    favourites_id: FavouritesId
    series_id: SeriesId
    created_at: datetime
