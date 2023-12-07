from amdb.domain.services.base import Service
from amdb.domain.entities.user.profile import Profile


class UnreviewSeries(Service):
    def __call__(
        self,
        *,
        profile: Profile,
    ) -> None:
        profile.series_reviews -= 1
