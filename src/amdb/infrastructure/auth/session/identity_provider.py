from typing import Optional

from amdb.domain.entities.user import UserId
from amdb.infrastructure.exception import InfrastructureError
from .gateway import SessionId, Session, SessionGateway


NO_SESSION_ID = "Session id is not passed"
SESSION_DOES_NOT_EXIST = "Session doesn't exist"


class SessionIdentityProvider:
    def __init__(
        self,
        *,
        session_id: Optional[SessionId],
        session_gateway: SessionGateway,
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

        session = self._session_gateway.get_session(
            session_id=self._session_id,
        )
        if not session:
            raise InfrastructureError(SESSION_DOES_NOT_EXIST)

        return session
