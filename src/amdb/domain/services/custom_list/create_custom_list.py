from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.custom_list.custom_list import CustomListId, CustomList
from amdb.domain.entities.user.profile import Profile


class CreateCustomList(Service):
    def __call__(
        self,
        *,
        profile: Profile,
        id: CustomListId,
        title: str,
        is_private: bool,
        created_at: datetime,
        description: Optional[str] = None,
    ) -> CustomList:
        return CustomList(
            id=id,
            user_id=profile.user_id,
            title=title,
            is_private=is_private,
            created_at=created_at,
            description=description,
            updated_at=None,
        )
