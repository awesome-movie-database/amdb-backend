from amdb.domain.entities.user import User
from amdb.application.common.constants.sending import SendingMethod
from amdb.application.common.constants.exceptions import USER_HAS_NO_EMAIL
from amdb.application.common.exception import ApplicationError


class EnsureCanUseSendingMethod:
    def __call__(
        self,
        *,
        user: User,
        sending_method: SendingMethod,
    ) -> None:
        if sending_method is SendingMethod.EMAIL and not user.email:
            raise ApplicationError(USER_HAS_NO_EMAIL)
