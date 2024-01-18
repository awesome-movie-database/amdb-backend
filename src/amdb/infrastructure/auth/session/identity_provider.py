from typing import Optional

from amdb.domain.entities.user import UserId
from amdb.infrastructure.persistence.redis.gateways.session import RedisSessionGateway
from amdb.infrastructure.exception import InfrastructureError
from .constants.exceptions import NO_SESSION_ID, SESSION_DOES_NOT_EXIST
from .model import SessionId, Session


class SessionIdentityProvider:
    def __init__(
        self,
        *,
        session_id: Optional[SessionId],
        session_gateway: RedisSessionGateway,
    ) -> None:
        self._session_id = session_id
        self._session_gateway = session_gateway

    def get_user_id(self) -> UserId:
        return self._get_session().user_id

    def get_permissions(self) -> int:
        return self._get_session().permissions

    def _get_session(self) -> Session:
        if not self._session_id:
            raise InfrastructureError(NO_SESSION_ID)

        session = self._session_gateway.with_id(self._session_id)
        if not session:
            raise InfrastructureError(SESSION_DOES_NOT_EXIST)

        return session
