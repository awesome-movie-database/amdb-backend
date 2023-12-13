from amdb.domain.services.base import Service
from amdb.domain.entities.review.series_review import SeriesReview
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.vote.series_review_vote import SeriesReviewVote
from amdb.domain.constants.common import VoteType


class UnvoteSeriesReview(Service):
    def __call__(
        self,
        *,
        series_review_vote: SeriesReviewVote,
        series_review: SeriesReview,
        reviewer_profile: Profile,
        voter_profile: Profile,
    ) -> None:
        voter_profile.given_votes -= 1
        reviewer_profile.gained_votes -= 1

        if series_review_vote.type is VoteType.LIKE:
            series_review.likes -= 1
        elif series_review_vote.type is VoteType.DISLIKE:
            series_review.dislikes -= 1
