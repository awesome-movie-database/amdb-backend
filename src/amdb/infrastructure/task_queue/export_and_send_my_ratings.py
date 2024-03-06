from amdb.domain.entities.user import UserId
from amdb.application.common.constants.export import ExportFormat
from amdb.application.common.constants.sending import SendingMethod


class EnqueueFakeExportAndSendingMyRatings:
    def __call__(
        self,
        *,
        user_id: UserId,
        export_format: ExportFormat,
        sending_method: SendingMethod,
    ) -> None:
        ...
