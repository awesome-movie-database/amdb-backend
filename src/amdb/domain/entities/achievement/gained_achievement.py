from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.user.user import UserId
from .achievement import AchievementId


@dataclass(slots=True)
class GainedAchievement(Entity):
    achievement_id: AchievementId
    user_id: UserId
    created_at: datetime
