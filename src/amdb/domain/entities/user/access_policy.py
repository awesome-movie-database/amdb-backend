from dataclasses import dataclass
from typing import Optional

from amdb.domain.entities.base import Entity
from amdb.domain.entities.user.user import UserId


@dataclass(slots=True)
class AccessPolicy(Entity):
    is_active: bool
    is_verified: bool


@dataclass(slots=True)
class AccessPolicyWithIdentity(AccessPolicy):
    id: UserId


@dataclass(slots=True)
class RequiredAccessPolicy(AccessPolicy):
    id: Optional[UserId]
