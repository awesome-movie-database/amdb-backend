import os

from amdb.domain.entities.user import UserId
from amdb.infrastructure.security.hasher import Hasher
from .model import SessionId, Session


class SessionProcessor:
    def __init__(
        self,
        hasher: Hasher,
    ) -> None:
        self._hasher = hasher

    def create(self, user_id: UserId, permissions: int) -> Session:
        random_hash = self._hasher.hash(os.urandom(32))
        return Session(
            id=SessionId(str(random_hash)),
            user_id=user_id,
            permissions=permissions,
        )
