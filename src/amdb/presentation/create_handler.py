__all__ = ("CreateHandler",)

from typing import TypeVar, Protocol

from amdb.application.common.identity_provider import IdentityProvider


H = TypeVar("H", covariant=True)


class CreateHandler(Protocol[H]):
    def __call__(
        self,
        identity_provider: IdentityProvider,
    ) -> H:
        raise NotImplementedError
