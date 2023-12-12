from amdb.domain.services.base import Service
from amdb.domain.entities.review.review_approval_policy import ReviewApprovalPolicy


class CheckReviewApproved(Service):
    def __call__(
        self,
        *,
        required_review_approval_policy: ReviewApprovalPolicy,
        current_review_approval_policy: ReviewApprovalPolicy,
    ) -> bool:
        if (
            required_review_approval_policy.is_verified
            and not current_review_approval_policy.is_verified
            and required_review_approval_policy.time_from_verification  # type: ignore
            > current_review_approval_policy.time_from_verification
        ):
            return False

        return (
            current_review_approval_policy.approved_review_count
            >= required_review_approval_policy.approved_review_count
            and current_review_approval_policy.time_from_creating
            >= required_review_approval_policy.time_from_creating
        )
