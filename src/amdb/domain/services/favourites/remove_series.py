from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.favourites.favourites import Favourites


class RemoveSeriesFromFavourites(Service):
    def __call__(
        self,
        *,
        favourites: Favourites,
        updated_at: datetime,
    ) -> None:
        favourites.updated_at = updated_at
