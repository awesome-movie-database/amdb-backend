from dataclasses import dataclass

from amdb.domain.policies.base import Policy


@dataclass(slots=True)
class SeriesSeasonReviewingPolicy(Policy):
    auto_approve: bool
