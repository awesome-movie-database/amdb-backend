from typing import Optional, cast

from amdb.domain.entities.user import UserId
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.infrastructure.exception import InfrastructureError
from .session import SessionId, Session
from .session_gateway import SessionGateway


NO_SESSION_ID = "Session id is not passed"
SESSION_DOES_NOT_EXIST = "Session doesn't exist"


class SessionIdentityProvider:
    def __init__(
        self,
        *,
        session_id: Optional[SessionId],
        session_gateway: SessionGateway,
        permissions_gateway: PermissionsGateway,
    ) -> None:
        self._session_id = session_id
        self._session_gateway = session_gateway
        self._permissions_gateway = permissions_gateway

    def user_id(self) -> UserId:
        return self._session().user_id

    def user_id_or_none(self) -> Optional[UserId]:
        session = self._session_or_none()
        return session.user_id if session else None

    def permissions(self) -> int:
        session = self._session()

        permissions = self._permissions_gateway.with_user_id(session.user_id)
        permissions = cast(int, permissions)

        return permissions

    def _session(self) -> Session:
        if not self._session_id:
            raise InfrastructureError(NO_SESSION_ID)

        session = self._session_gateway.with_id(self._session_id)
        if not session:
            raise InfrastructureError(SESSION_DOES_NOT_EXIST)

        return session

    def _session_or_none(self) -> Optional[Session]:
        if self._session_id:
            return self._session_gateway.with_id(self._session_id)
        return None
