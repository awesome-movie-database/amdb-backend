from dataclasses import dataclass
from typing import NewType

from amdb.domain.entities.user import UserId


SessionId = NewType("SessionId", str)


@dataclass(frozen=True, slots=True)
class Session:
    id: SessionId
    user_id: UserId
    permissions: int
