from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.favourites.favourites import Favourites


class RemoveMovieFromFavourites(Service):
    def __call__(
        self,
        *,
        favourites: Favourites,
        timestamp: datetime,
    ) -> None:
        favourites.updated_at = timestamp
