from typing import Optional, cast

from amdb.domain.entities.user import UserId
from amdb.infrastructure.persistence.redis.gateways.session import (
    RedisSessionGateway,
)
from amdb.infrastructure.persistence.redis.gateways.permissions import (
    RedisPermissionsGateway,
)
from amdb.infrastructure.exception import InfrastructureError
from .constants.exceptions import NO_SESSION_ID, SESSION_DOES_NOT_EXIST
from .model import SessionId


class SessionIdentityProvider:
    def __init__(
        self,
        *,
        session_id: Optional[SessionId],
        session_gateway: RedisSessionGateway,
        permissions_gateway: RedisPermissionsGateway,
    ) -> None:
        self._session_id = session_id
        self._session_gateway = session_gateway
        self._permissions_gateway = permissions_gateway

    def get_user_id(self) -> UserId:
        return self._get_user_id()

    def get_permissions(self) -> int:
        user_id = self._get_user_id()
        permissions = self._permissions_gateway.with_user_id(user_id)
        permissions = cast(int, permissions)

        return permissions

    def _get_user_id(self) -> UserId:
        if not self._session_id:
            raise InfrastructureError(NO_SESSION_ID)

        session = self._session_gateway.with_id(self._session_id)
        if not session:
            raise InfrastructureError(SESSION_DOES_NOT_EXIST)

        return session.user_id
