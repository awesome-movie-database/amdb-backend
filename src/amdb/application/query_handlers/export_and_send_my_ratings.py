from amdb.domain.entities.user import User
from amdb.application.common.constants.sending import SendingMethod
from amdb.application.common.entities.file import File
from amdb.application.common.services.ensure_can_use import (
    EnsureCanUseSendingMethod,
)
from amdb.application.common.services.convert_to_file import (
    ConvertMyRatingsToFile,
)
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.readers.rating_for_export import (
    RatingForExportViewModelsReader,
)
from amdb.application.common.sending.email import SendEmail
from amdb.application.common.constants.exceptions import USER_DOES_NOT_EXIST
from amdb.application.common.exception import ApplicationError
from amdb.application.queries.export_and_send_my_ratings import (
    ExportAndSendMyRatingsQuery,
)


class ExportAndSendMyRatingsHandler:
    def __init__(
        self,
        *,
        ensure_can_use_sending_method: EnsureCanUseSendingMethod,
        convert_my_ratings_to_file: ConvertMyRatingsToFile,
        user_gateway: UserGateway,
        ratings_for_export_reader: RatingForExportViewModelsReader,
        send_email: SendEmail,
    ) -> None:
        self._ensure_can_use_sending_method = ensure_can_use_sending_method
        self._convert_my_ratings_to_file = convert_my_ratings_to_file
        self._user_gateway = user_gateway
        self._ratings_for_export_reader = ratings_for_export_reader
        self._send_email = send_email

    def execute(self, query: ExportAndSendMyRatingsQuery) -> None:
        user = self._user_gateway.with_id(query.user_id)
        if not user:
            raise ApplicationError(USER_DOES_NOT_EXIST)

        self._ensure_can_use_sending_method(
            user=user,
            sending_method=query.sending_method,
        )
        view_models = self._ratings_for_export_reader.get(
            current_user_id=query.user_id,
        )
        file = self._convert_my_ratings_to_file(
            view_models=view_models,
            format=query.format,
        )
        self._send_file(
            user=user,
            file=file,
            sending_method=query.sending_method,
        )

    def _send_file(
        self,
        *,
        user: User,
        file: File,
        sending_method: SendingMethod,
    ) -> None:
        if sending_method is SendingMethod.EMAIL and user.email:
            self._send_email(
                email=user.email,
                subject="Your exported ratings",
                files=[file],
            )
