from dataclasses import dataclass
from datetime import datetime
from typing import Optional, NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.entities.user.user import UserId


FavouritesId = NewType("FavouritesId", UUID)


@dataclass(slots=True)
class Favourites(Entity):
    id: FavouritesId
    user_id: UserId
    is_private: bool

    updated_at: Optional[datetime]
