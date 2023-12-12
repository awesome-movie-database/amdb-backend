from dataclasses import dataclass

from amdb.domain.entities.base import Entity
from amdb.domain.entities.user.user import UserId


@dataclass(slots=True)
class AccessPolicy(Entity):
    id: UserId
    is_active: bool
    is_verified: bool
