from amdb.domain.services.base import Service
from amdb.domain.entities.review.series_season_review import SeriesSeasonReview
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.vote.series_season_review_vote import SeriesSeasonReviewVote
from amdb.domain.constants.common import VoteType
from amdb.domain.constants.exceptions import SERIES_SEASON_REVIEW_NOT_APPROVED
from amdb.domain.exception import DomainError


class VoteSeriesSeasonReview(Service):
    def __call__(
        self,
        *,
        season_review: SeriesSeasonReview,
        reviewer_profile: Profile,
        voter_profile: Profile,
        type: VoteType,
    ) -> SeriesSeasonReviewVote:
        if not season_review.is_approved:
            raise DomainError(SERIES_SEASON_REVIEW_NOT_APPROVED)

        voter_profile.given_votes += 1
        reviewer_profile.gained_votes += 1

        if type is VoteType.LIKE:
            season_review.likes += 1
        elif type is VoteType.DISLIKE:
            season_review.dislikes += 1

        return SeriesSeasonReviewVote(
            series_season_review_id=season_review.id,
            user_id=voter_profile.user_id,
            type=type,
        )
