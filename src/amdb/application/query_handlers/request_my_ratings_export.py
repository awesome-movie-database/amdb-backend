from typing import cast

from amdb.domain.entities.user import User
from amdb.application.common.services.ensure_can_use import (
    EnsureCanUseSendingMethod,
)
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.task_queue.export_and_send_my_ratings import (
    EnqueueExportAndSendingMyRatings,
)
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.queries.request_my_ratings_export import (
    RequestMyRatingsExportQuery,
)


class RequestMyRatingsExportHandler:
    def __init__(
        self,
        *,
        ensure_can_use_sending_method: EnsureCanUseSendingMethod,
        user_gateway: UserGateway,
        enqueue_export_and_sending: EnqueueExportAndSendingMyRatings,
        identity_provider: IdentityProvider,
    ) -> None:
        self._ensure_can_use_sending_method = ensure_can_use_sending_method
        self._user_gateway = user_gateway
        self._enqueue_export_and_sending = enqueue_export_and_sending
        self._identity_provider = identity_provider

    def execute(self, query: RequestMyRatingsExportQuery) -> None:
        current_user_id = self._identity_provider.user_id()

        user = self._user_gateway.with_id(current_user_id)
        user = cast(User, user)

        self._ensure_can_use_sending_method(
            user=user,
            sending_method=query.sending_method,
        )
        self._enqueue_export_and_sending(
            user_id=current_user_id,
            export_format=query.format,
            sending_method=query.sending_method,
        )
