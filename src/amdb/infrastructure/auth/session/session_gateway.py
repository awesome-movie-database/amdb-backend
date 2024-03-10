from typing import Optional, Protocol

from .session import SessionId, Session


class SessionGateway(Protocol):
    def with_id(self, session_id: SessionId) -> Optional[Session]:
        raise NotImplementedError
