from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .base import Policy


@dataclass(slots=True)
class AccessPolicy(Policy):
    user_id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
