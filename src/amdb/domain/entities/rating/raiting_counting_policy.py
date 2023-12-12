from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from amdb.domain.entities.base import Entity


@dataclass(slots=True)
class RatingCountingPolicy(Entity):
    is_verified: bool
    time_from_creating: timedelta
    rating_count: int

    time_from_verification: Optional[datetime]
