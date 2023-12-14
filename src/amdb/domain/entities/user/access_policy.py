from dataclasses import dataclass
from typing import Optional

from amdb.domain.entities.base import Entity
from amdb.domain.entities.user.user import UserId


@dataclass(slots=True)
class AccessPolicyWithIdentity(Entity):
    id: UserId
    is_active: bool
    is_verified: bool


@dataclass(slots=True)
class RequiredAccessPolicy(Entity):
    id: Optional[UserId]
    is_active: Optional[bool]
    is_verified: Optional[bool]
