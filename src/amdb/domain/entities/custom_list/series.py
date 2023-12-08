from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.series.series import SeriesId
from .custom_list import CustomListId


@dataclass(slots=True)
class CustomListSeries(Entity):
    custom_list_id: CustomListId
    series_id: SeriesId
    created_at: datetime
