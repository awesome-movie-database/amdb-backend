from typing import TypeVar, Protocol

from amdb.application.common.identity_provider import IdentityProvider


_H = TypeVar("_H", covariant=True)


class CreateHandler(Protocol[_H]):
    def __call__(
        self,
        identity_provider: IdentityProvider,
    ) -> _H:
        raise NotImplementedError
