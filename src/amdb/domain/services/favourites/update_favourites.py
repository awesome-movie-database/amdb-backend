from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.favourites.favourites import Favourites


class UpdateFavourites(Service):
    def __call__(
        self,
        *,
        favourites: Favourites,
        is_private: bool,
        updated_at: datetime,
    ) -> None:
        favourites.is_private = is_private
        favourites.updated_at = updated_at
