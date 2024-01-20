from uuid import uuid4

from amdb.domain.entities.user import UserId
from .model import SessionId, Session


class SessionProcessor:
    def create(self, user_id: UserId) -> Session:
        session_id = uuid4().hex + uuid4().hex
        return Session(
            id=SessionId(session_id),
            user_id=user_id,
        )
