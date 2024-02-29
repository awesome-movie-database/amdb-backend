from unittest.mock import Mock
from typing import Optional

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import User, UserId
from amdb.application.common.constants.export import ExportFormat
from amdb.application.common.constants.sending import SendingMethod
from amdb.application.common.services.ensure_can_use_sending_method import (
    EnsureCanUseSendingMethod,
)
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.task_queue.export_and_send_my_ratings import (
    EnqueueExportAndSendingMyRatings,
)
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import (
    USER_HAS_NO_EMAIL,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.queries.request_my_ratings_export import (
    RequestMyRatingsExportQuery,
)
from amdb.application.query_handlers.request_my_ratings_export import (
    RequestMyRatingsExportHandler,
)


def test_request_my_ratings_export(
    user_gateway: UserGateway,
    unit_of_work: UnitOfWork,
):
    user = User(
        id=UserId(uuid7()),
        name="John Doe",
        email="John@doe.com",
    )
    user_gateway.save(user)

    unit_of_work.commit()

    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id = Mock(
        return_value=user.id,
    )
    enqueue_export_and_sending: EnqueueExportAndSendingMyRatings = Mock()

    query = RequestMyRatingsExportQuery(
        format=ExportFormat.CSV,
        sending_method=SendingMethod.EMAIL,
    )
    handler = RequestMyRatingsExportHandler(
        ensure_can_use_sending_method=EnsureCanUseSendingMethod(),
        user_gateway=user_gateway,
        enqueue_export_and_sending=enqueue_export_and_sending,
        identity_provider=identity_provider,
    )

    handler.execute(query)


@pytest.mark.parametrize(
    (
        "sending_method",
        "email",
    ),
    (
        (
            SendingMethod.EMAIL,
            None,
        ),
    ),
)
def test_request_my_ratings_export_should_raise_error_when_user_cannot_use_sending_method(
    sending_method: SendingMethod,
    email: Optional[str],
    user_gateway: UserGateway,
    unit_of_work: UnitOfWork,
):
    user = User(
        id=UserId(uuid7()),
        name="John Doe",
        email=email,
    )
    user_gateway.save(user)

    unit_of_work.commit()

    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id = Mock(
        return_value=user.id,
    )
    enqueue_export_and_sending: EnqueueExportAndSendingMyRatings = Mock()

    query = RequestMyRatingsExportQuery(
        format=ExportFormat.CSV,
        sending_method=sending_method,
    )
    handler = RequestMyRatingsExportHandler(
        ensure_can_use_sending_method=EnsureCanUseSendingMethod(),
        user_gateway=user_gateway,
        enqueue_export_and_sending=enqueue_export_and_sending,
        identity_provider=identity_provider,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(query)

    assert error.value.message == USER_HAS_NO_EMAIL
