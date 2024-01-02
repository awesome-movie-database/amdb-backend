from dataclasses import dataclass
from datetime import timedelta
from typing import NewType, Optional
from uuid import UUID, uuid4

from redis import Redis

from amdb.domain.entities.user import UserId


SessionId = NewType("SessionId", str)


@dataclass(frozen=True, slots=True)
class Session:
    user_id: UserId
    permissions: int


class SessionGateway:
    def __init__(
        self,
        redis: Redis,
        session_lifetime: timedelta,
    ) -> None:
        self._redis = redis
        self._session_lifetime = session_lifetime

    def save_session(self, session: Session) -> SessionId:
        session_id = uuid4().hex,
        session_data = {
            "user_id": session.user_id.hex,
            "permissions": session.permissions
        }
        self._redis.hset(
            name=session_id,
            mapping=session_data,
        )
        self._redis.expire(
            name=session_id,
            time=self._session_lifetime,
        )

        return session_id

    def get_session(self, session_id: SessionId) -> Optional[Session]:
        session_data = self._redis.hgetall(session_id)
        if session_data:
            return Session(
                user_id=UserId(UUID(session_data["user_id"])),
                permissions=session_data["permissions"],
            )
        return None
