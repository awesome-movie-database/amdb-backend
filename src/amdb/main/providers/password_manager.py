from dishka import Provider, Scope, provide

from amdb.application.common.password_manager import PasswordManager
from amdb.infrastructure.password_manager.hash_computer import HashComputer
from amdb.infrastructure.password_manager.password_hash_gateway import (
    PasswordHashGateway,
)
from amdb.infrastructure.password_manager.password_manager import (
    HashingPasswordManager,
)


class PasswordManagerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def password_manager(
        self,
        password_hash_gateway: PasswordHashGateway,
    ) -> PasswordManager:
        return HashingPasswordManager(
            hash_computer=HashComputer(),
            password_hash_gateway=password_hash_gateway,
        )
