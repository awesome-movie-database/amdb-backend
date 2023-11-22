from dataclasses import dataclass

from .base import Policy


@dataclass(slots=True)
class MovieReviewingPolicy(Policy):
    auto_approve: bool
