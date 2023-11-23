from dataclasses import dataclass
from datetime import datetime, timedelta

from amdb.domain.policies.base import Policy


@dataclass(slots=True)
class SeriesEpisodeVotingPolicy(Policy):
    must_be_active: bool
    must_be_verified: bool
    required_days_since_registration: int
    required_vote_count: int

    def check_can_create_full_vote(
        self,
        is_active: bool,
        is_verified: bool,
        created_at: datetime,
        vote_count: int,
    ) -> bool:
        cannot_create_full_vote = (
            not is_active
            and self.must_be_active
            or not is_verified
            and self.must_be_verified
            or datetime.utcnow() - created_at
            < timedelta(days=self.required_days_since_registration)
            or vote_count < self.required_vote_count
        )
        return not cannot_create_full_vote
