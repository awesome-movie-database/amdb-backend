from dataclasses import dataclass
from datetime import datetime
from typing import Optional, NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.entities.user.user import UserId


CustomListId = NewType("CustomListId", UUID)


@dataclass(slots=True)
class CustomList(Entity):
    id: CustomListId
    user_id: UserId
    title: str
    is_private: bool
    created_at: datetime

    description: Optional[str]
    updated_at: Optional[datetime]
