from dishka import Provider, Scope, provide
from redis import Redis

from amdb.infrastructure.auth.session.config import SessionConfig
from amdb.infrastructure.auth.session.session_processor import SessionProcessor
from amdb.infrastructure.auth.session.session_gateway import SessionGateway
from amdb.infrastructure.persistence.redis.mappers.session import SessionMapper


class SessionAdaptersProvider(Provider):
    scope = Scope.APP

    def __init__(self, session_config: SessionConfig) -> None:
        super().__init__()
        self._session_config = session_config

    @provide
    def session_config(self) -> SessionConfig:
        return self._session_config

    @provide
    def session_processor(self) -> SessionProcessor:
        return SessionProcessor()

    @provide
    def session_gateway(self, redis: Redis) -> SessionGateway:
        return SessionMapper(
            redis=redis,
            session_lifetime=self._session_config.lifetime,
        )
