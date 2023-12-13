from amdb.domain.services.base import Service
from amdb.domain.entities.review.series_episode_review import SeriesEpisodeReview
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.vote.series_episode_review_vote import SeriesEpisodeReviewVote
from amdb.domain.constants.common import VoteType


class UnvoteSeriesEpisodeReview(Service):
    def __call__(
        self,
        *,
        episode_review_vote: SeriesEpisodeReviewVote,
        episode_review: SeriesEpisodeReview,
        reviewer_profile: Profile,
        voter_profile: Profile,
    ) -> None:
        voter_profile.given_votes -= 1
        reviewer_profile.gained_votes -= 1

        if episode_review_vote.type is VoteType.LIKE:
            episode_review.likes -= 1
        elif episode_review_vote.type is VoteType.DISLIKE:
            episode_review.dislikes -= 1
