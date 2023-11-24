from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from amdb.domain.exceptions.acess import AccessDenied
from .base import Policy


@dataclass(slots=True)
class AccessPolicy(Policy):
    user_id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime

    def ensure_can_vote(self) -> None:
        if not self.is_active:
            raise AccessDenied()
    
    def ensure_can_review(self) -> None:
        if not self.is_active:
            raise AccessDenied()
    
    def ensure_can_rate_reviews(self) -> None:
        if not self.is_active:
            raise AccessDenied()