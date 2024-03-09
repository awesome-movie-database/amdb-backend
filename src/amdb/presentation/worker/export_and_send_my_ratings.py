from typing import Annotated

from dishka.integrations.faststream import FromDishka, inject

from amdb.domain.entities.user import UserId
from amdb.application.common.constants.export import ExportFormat
from amdb.application.common.constants.sending import SendingMethod
from amdb.application.queries.export_and_send_my_ratings import (
    ExportAndSendMyRatingsQuery,
)
from amdb.application.query_handlers.export_and_send_my_ratings import (
    ExportAndSendMyRatingsHandler,
)


@inject
async def export_and_send_my_ratings(
    handler: Annotated[ExportAndSendMyRatingsHandler, FromDishka()],
    user_id: UserId,
    export_format: ExportFormat,
    sending_method: SendingMethod,
) -> None:
    query = ExportAndSendMyRatingsQuery(
        user_id=user_id,
        format=export_format,
        sending_method=sending_method,
    )
    handler.execute(query)
