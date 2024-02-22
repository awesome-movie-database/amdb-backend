from datetime import timedelta
from typing import Optional, cast
from uuid import UUID

from redis import Redis

from amdb.domain.entities.user import UserId
from amdb.infrastructure.auth.session.session import SessionId, Session


class SessionMapper:
    def __init__(
        self,
        *,
        redis: Redis,
        session_lifetime: timedelta,
    ) -> None:
        self._redis = redis
        self._session_lifetime = session_lifetime

    def save(self, session: Session) -> SessionId:
        self._redis.set(
            name=f"user_id:session_id:{session.id}",
            value=session.user_id.hex,
        )
        self._redis.expire(
            name=f"user_id:session_id:{session.id}",
            time=self._session_lifetime,
        )
        return session.id

    def with_id(self, session_id: SessionId) -> Optional[Session]:
        user_id = self._redis.get(f"user_id:session_id:{session_id}")
        if user_id:
            return Session(
                id=session_id,
                user_id=UserId(UUID(cast(str, user_id))),
            )
        return None
