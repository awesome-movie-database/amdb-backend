from amdb.domain.services.base import Service
from amdb.domain.entities.review.series_season_review import SeriesSeasonReview
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.vote.series_season_review_vote import SeriesSeasonReviewVote
from amdb.domain.constants import VoteType


class UnvoteSeriesSeasonReview(Service):
    def __call__(
        self,
        *,
        season_review_vote: SeriesSeasonReviewVote,
        season_review: SeriesSeasonReview,
        reviewer_profile: Profile,
        voter_profile: Profile,
    ) -> None:
        voter_profile.given_votes -= 1
        reviewer_profile.gained_votes -= 1

        if season_review_vote.type is VoteType.LIKE:
            season_review.likes -= 1
        elif season_review_vote.type is VoteType.DISLIKE:
            season_review.dislikes -= 1
