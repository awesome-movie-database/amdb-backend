from uuid import uuid4

from amdb.domain.entities.user import UserId
from .session import SessionId, Session


class SessionProcessor:
    def create(self, user_id: UserId) -> Session:
        return Session(
            id=self._gen_session_id(),
            user_id=user_id,
        )

    def _gen_session_id(self) -> SessionId:
        random_value = uuid4().hex + uuid4().hex + uuid4().hex
        return SessionId(random_value)
