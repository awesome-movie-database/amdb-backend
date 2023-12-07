from amdb.domain.services.base import Service
from amdb.domain.entities.user.profile import Profile


class UnreviewSeriesEpisode(Service):
    def __call__(
        self,
        *,
        profile: Profile,
    ) -> None:
        profile.series_episode_ratings -= 1
