from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.series.series import SeriesId
from .list import ListId


@dataclass(slots=True)
class ListSeries(Entity):
    list_id: ListId
    series_id: SeriesId
    created_at: datetime
