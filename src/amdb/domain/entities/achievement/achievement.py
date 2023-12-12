from dataclasses import dataclass
from typing import NewType
from enum import IntEnum
from uuid import UUID

from amdb.domain.entities.base import Entity


AchievementId = NewType("AchievementId", UUID)


class AchievementType(IntEnum):
    RATING_MOVIES = 0
    RATING_SERIES_EPISODES = 1
    REVIEWING_MOVIES = 2
    REVIEWING_SERIES_EPISODES = 3
    VOTING_REVIEWS = 4
    GAINED_REVIEW_VOTES = 5


@dataclass(slots=True)
class Achievement(Entity):
    id: AchievementId
    title: str
    description: str
    type: AchievementType
