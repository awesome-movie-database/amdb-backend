from amdb.domain.services.base import Service
from amdb.domain.entities.review.movie_review import MovieReview
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.vote.movie_review_vote import MovieReviewVote
from amdb.domain.constants import VoteType


class VoteMovieReview(Service):
    def __call__(
        self,
        *,
        movie_review: MovieReview,
        profile: Profile,
        type: VoteType
    ) -> MovieReviewVote:
        profile.given_votes += 1

        return MovieReviewVote(
            movie_review_id=movie_review.id,
            user_id=profile.user_id,
            type=type,
        )