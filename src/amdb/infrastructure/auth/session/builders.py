from redis import Redis

from .config import SessionIdentityProviderConfig
from .gateway import SessionGateway


def build_session_gateway(
    session_identity_provider_config: SessionIdentityProviderConfig,
) -> SessionGateway:
    redis = Redis(
        host=session_identity_provider_config.redis_host,
        port=session_identity_provider_config.redis_port,
        db=session_identity_provider_config.redis_db,
        password=session_identity_provider_config.redis_password,
    )
    return SessionGateway(
        redis=redis,
        session_lifetime=session_identity_provider_config.session_lifetime,
    )
