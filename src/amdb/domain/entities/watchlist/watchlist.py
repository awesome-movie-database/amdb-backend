from dataclasses import dataclass
from datetime import datetime
from typing import Optional, NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.entities.user.user import UserId


WatchlistId = NewType("WatchlistId", UUID)


@dataclass(slots=True)
class Watchlist(Entity):
    id: WatchlistId
    user_id: UserId
    is_private: bool
    created_at: datetime

    updated_at: Optional[datetime]
