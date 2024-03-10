from dataclasses import dataclass

from amdb.application.common.constants.export import ExportFormat
from amdb.application.common.constants.sending import SendingMethod


@dataclass(frozen=True, slots=True)
class RequestMyRatingsExportQuery:
    format: ExportFormat
    sending_method: SendingMethod
