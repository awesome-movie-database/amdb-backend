from dataclasses import dataclass

from amdb.domain.policies.base import Policy


@dataclass(slots=True)
class ReviewingPolicy(Policy):
    auto_approve: bool
