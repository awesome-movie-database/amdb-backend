from amdb.domain.services.base import Service
from amdb.domain.entities.achievement.achievement import (
    AchievementId,
    AchievementType,
    Achievement,
)


class CreateAchievement(Service):
    def __call__(
        self,
        *,
        id: AchievementId,
        title: str,
        description: str,
        type: AchievementType,
    ) -> Achievement:
        return Achievement(
            id=id,
            title=title,
            description=description,
            type=type,
        )
