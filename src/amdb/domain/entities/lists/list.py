from dataclasses import dataclass
from datetime import datetime
from typing import Optional, NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.entities.user.user import UserId


ListId = NewType("ListId", UUID)


@dataclass(slots=True)
class List(Entity):
    id: ListId
    user_id: UserId
    title: str
    description: str
    is_private: bool
    created_at: datetime

    updated_at: Optional[datetime]
