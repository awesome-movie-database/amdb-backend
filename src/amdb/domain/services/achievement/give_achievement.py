from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.achievement.achievement import Achievement
from amdb.domain.entities.achievement.gained_achievement import GainedAchievement


class GiveAchievement(Service):
    def __call__(
        self,
        *,
        profile: Profile,
        achievement: Achievement,
        created_at: datetime,
    ) -> GainedAchievement:
        profile.achievements += 1

        return GainedAchievement(
            achievement_id=achievement.id,
            user_id=profile.user_id,
            created_at=created_at,
        )
