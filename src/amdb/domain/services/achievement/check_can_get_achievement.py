import dataclasses

from amdb.domain.services.base import Service
from amdb.domain.entities.achievement.achievement_progress import AchievementProgress


class CheckCanGetAchievement(Service):
    def __call__(
        self,
        *,
        required_achievement_progress: AchievementProgress,
        current_achievement_progress: AchievementProgress,
    ) -> bool:
        required = dataclasses.asdict(required_achievement_progress)
        current = dataclasses.asdict(current_achievement_progress)

        for name, min_value in required.items():
            if min_value is not None and min_value > current.get(name):
                return False

        return True
