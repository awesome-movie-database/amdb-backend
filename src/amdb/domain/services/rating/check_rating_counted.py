from amdb.domain.services.base import Service
from amdb.domain.entities.rating.raiting_counting_policy import RatingCountingPolicy


class CheckRatingCounted(Service):
    def __call__(
        self,
        *,
        required_rating_counting_policy: RatingCountingPolicy,
        current_rating_counting_policy: RatingCountingPolicy,
    ) -> bool:
        if (
            required_rating_counting_policy.is_verified
            and not current_rating_counting_policy.is_verified
            and required_rating_counting_policy.time_from_verification  # type: ignore
            > current_rating_counting_policy.time_from_verification
        ):
            return False

        return (
            current_rating_counting_policy.rating_count
            >= required_rating_counting_policy.rating_count
            and current_rating_counting_policy.time_from_creating
            >= required_rating_counting_policy.time_from_creating
        )
