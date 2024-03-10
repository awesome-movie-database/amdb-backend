from dataclasses import dataclass

from amdb.application.common.constants.export import ExportFormat


@dataclass(frozen=True, slots=True)
class ExportMyRatingsQuery:
    format: ExportFormat
