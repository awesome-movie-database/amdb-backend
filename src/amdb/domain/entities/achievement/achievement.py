from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from amdb.domain.entities.base import Entity


AchievementId = NewType("AchievementId", UUID)


@dataclass(slots=True)
class Achievement(Entity):
    id: AchievementId
    title: str
    description: str
