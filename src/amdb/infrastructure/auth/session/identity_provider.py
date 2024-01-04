from typing import Optional

from amdb.domain.entities.user import UserId
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.infrastructure.auth.exception import AuthenticationError
from .gateway import SessionId, Session, SessionGateway


class SessionIdentityProvider(IdentityProvider):
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
            raise AuthenticationError()

        session = self._session_gateway.get_session(
            session_id=self._session_id,
        )
        if not session:
            raise AuthenticationError()

        return session
