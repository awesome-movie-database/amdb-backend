from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.entities.achievement.achievement import Achievement
from amdb.domain.constants.common import Unset, unset


class UpdateAchievement(Service):
    def __call__(
        self,
        *,
        achievement: Achievement,
        title: Union[str, Unset] = unset,
        description: Union[str, Unset] = unset,
    ) -> None:
        self._update_entity(
            entity=achievement,
            title=title,
            description=description,
        )
