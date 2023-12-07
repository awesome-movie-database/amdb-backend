from amdb.domain.services.base import Service
from amdb.domain.entities.review.series_episode_review import SeriesEpisodeReview
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.vote.series_episode_review_vote import SeriesEpisodeReviewVote
from amdb.domain.constants import VoteType
from amdb.domain.exceptions.review import SeriesEpisodeReviewNotApprovedError


class VoteSeriesEpisodeReview(Service):
    def __call__(
        self,
        *,
        series_episode_review: SeriesEpisodeReview,
        reviewer_profile: Profile,
        voter_profile: Profile,
        type: VoteType,
    ) -> SeriesEpisodeReviewVote:
        if not series_episode_review.is_approved:
            raise SeriesEpisodeReviewNotApprovedError()

        voter_profile.given_votes += 1
        reviewer_profile.gained_votes += 1

        if type is VoteType.LIKE:
            series_episode_review.likes += 1
        elif type is VoteType.DISLIKE:
            series_episode_review.dislikes += 1

        return SeriesEpisodeReviewVote(
            series_episode_review_id=series_episode_review.id,
            user_id=voter_profile.user_id,
            type=type,
        )
