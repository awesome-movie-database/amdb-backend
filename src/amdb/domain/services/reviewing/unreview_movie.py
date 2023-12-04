from amdb.domain.services.base import Service
from amdb.domain.entities.user.profile import Profile


class UnreviewMovie(Service):
    def __call__(
        self,
        *,
        profile: Profile,
    ) -> None:
        profile.movie_ratings -= 1