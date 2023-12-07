from amdb.domain.services.base import Service
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.favourites.favourites import FavouritesId, Favourites


class CreateFavourites(Service):
    def __call__(
        self,
        *,
        profile: Profile,
        id: FavouritesId,
    ) -> Favourites:
        return Favourites(
            id=id,
            user_id=profile.user_id,
            is_private=False,
            updated_at=None,
        )
