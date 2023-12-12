from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.user.user import UserId


@dataclass(slots=True)
class AccessPolicy(Entity):
    id: UserId
    is_active: bool
    is_verified: bool
    created_at: datetime
    verified_at: datetime
