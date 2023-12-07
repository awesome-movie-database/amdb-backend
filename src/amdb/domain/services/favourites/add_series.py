from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.favourites.favourites import Favourites
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.favourites.series import FavouriteSeries


class AddSeriesToFavourites(Service):
    def __call__(
        self,
        *,
        favourites: Favourites,
        series: Series,
        created_at: datetime,
    ) -> FavouriteSeries:
        favourites.updated_at = created_at

        return FavouriteSeries(
            favourites_id=favourites.id,
            series_id=series.id,
            created_at=created_at,
        )
