from amdb.domain.services.base import Service
from amdb.domain.entities.user.user import User
from amdb.domain.entities.user.profile import Profile


class CreateProfile(Service):
    def __call__(
        self,
        *,
        user: User,
    ) -> Profile:
        return Profile(
            user_id=user.id,
            achievements=0,
            movie_ratings=0,
            series_episodes_ratings=0,
            movie_reviews=0,
            series_reviews=0,
            given_votes=0,
            gained_votes=0,
        )
