from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from amdb.domain.entities.base import Entity


@dataclass(slots=True)
class ReviewApprovalProgress(Entity):
    is_verified: bool
    time_from_creating: datetime
    approved_review_count: int

    time_from_verification: Optional[datetime]
