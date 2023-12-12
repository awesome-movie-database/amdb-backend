from amdb.domain.services.base import Service
from amdb.domain.entities.review.review_approval_progress import ReviewApprovalProgress


class CheckReviewApproved(Service):
    def __call__(
        self,
        *,
        required_review_approval_progress: ReviewApprovalProgress,
        current_review_approval_progress: ReviewApprovalProgress,
    ) -> bool:
        if (
            required_review_approval_progress.is_verified
            and not current_review_approval_progress.is_verified
            and required_review_approval_progress.time_from_verification  # type: ignore
            > current_review_approval_progress.time_from_verification
        ):
            return False

        return (
            current_review_approval_progress.approved_review_count
            >= required_review_approval_progress.approved_review_count
            and current_review_approval_progress.time_from_creating
            >= required_review_approval_progress.time_from_creating
        )
