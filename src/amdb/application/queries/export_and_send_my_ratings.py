from dataclasses import dataclass

from amdb.domain.entities.user import UserId
from amdb.application.common.constants.export import ExportFormat
from amdb.application.common.constants.sending import SendingMethod


@dataclass(frozen=True, slots=True)
class ExportAndSendMyRatingsQuery:
    user_id: UserId
    format: ExportFormat
    sending_method: SendingMethod
