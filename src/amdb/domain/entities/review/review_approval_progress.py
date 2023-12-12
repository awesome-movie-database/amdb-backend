from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from amdb.domain.entities.base import Entity


@dataclass(slots=True)
class ReviewApprovalProgress(Entity):
    is_verified: bool
    time_from_creating: timedelta
    approved_review_count: int

    time_from_verification: Optional[timedelta]
