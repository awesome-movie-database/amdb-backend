from amdb.domain.services.base import Service
from amdb.domain.entities.review.movie_review import MovieReview
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.vote.movie_review_vote import MovieReviewVote
from amdb.domain.constants import VoteType
from amdb.domain.exceptions.review import MovieReviewNotApprovedError


class VoteMovieReview(Service):
    def __call__(
        self,
        *,
        movie_review: MovieReview,
        reviewer_profile: Profile,
        voter_profile: Profile,
        type: VoteType,
    ) -> MovieReviewVote:
        if not movie_review.is_approved:
            raise MovieReviewNotApprovedError()

        voter_profile.given_votes += 1
        reviewer_profile.gained_votes += 1

        if type is VoteType.LIKE:
            movie_review.likes += 1
        elif type is VoteType.DISLIKE:
            movie_review.dislikes += 1

        return MovieReviewVote(
            movie_review_id=movie_review.id,
            user_id=voter_profile.user_id,
            type=type,
        )
