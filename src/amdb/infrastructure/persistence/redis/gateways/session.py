from datetime import timedelta
from typing import Optional
from uuid import UUID

from redis import Redis

from amdb.domain.entities.user import UserId
from amdb.infrastructure.auth.session.model import SessionId, Session


class RedisSessionGateway:
    def __init__(
        self,
        *,
        redis: Redis,
        session_lifetime: timedelta,
    ) -> None:
        self._redis = redis
        self._session_lifetime = session_lifetime

    def save(self, session: Session) -> SessionId:
        session_data = {
            "user_id": session.user_id.hex,
            "permissions": session.permissions,
        }
        self._redis.hset(
            name=session.id,
            mapping=session_data,  # type: ignore
        )
        self._redis.expire(
            name=session.id,
            time=self._session_lifetime,
        )

        return session.id

    def with_id(self, session_id: SessionId) -> Optional[Session]:
        session_data = self._redis.hgetall(session_id)
        if session_data:
            return Session(
                id=session_id,
                user_id=UserId(UUID(session_data["user_id"])),
                permissions=session_data["permissions"],
            )
        return None
