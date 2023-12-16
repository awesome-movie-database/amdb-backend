from dataclasses import dataclass
from typing import Union
from enum import Enum

from amdb.domain.entities.base import Entity
from amdb.domain.entities.user.user import UserId


NoMatter = Enum("NoMatter", ["no_matter"])
no_matter = NoMatter.no_matter


@dataclass(slots=True)
class AccessPolicy(Entity):
    id: UserId
    is_active: bool
    is_verified: bool


@dataclass(slots=True)
class RequiredAccessPolicy(Entity):
    id: Union[UserId, NoMatter]
    is_active: Union[bool, NoMatter]
    is_verified: Union[bool, NoMatter]
