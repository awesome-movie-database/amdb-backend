from amdb.domain.services.base import Service
from amdb.domain.entities.review.movie_review import MovieReview
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.vote.movie_review_vote import MovieReviewVote
from amdb.domain.constants import VoteType


class UnvoteMovieReview(Service):
    def __call__(
        self,
        *,
        movie_review_vote: MovieReviewVote,
        movie_review: MovieReview,
        reviewer_profile: Profile,
        voter_profile: Profile,
    ) -> None:
        voter_profile.given_votes -= 1
        reviewer_profile.gained_votes -= 1

        if movie_review_vote.type is VoteType.LIKE:
            movie_review.likes += 1
        elif movie_review_vote.type is VoteType.DISLIKE:
            movie_review.dislikes += 1
