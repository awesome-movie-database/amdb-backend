from dishka import Provider, Scope, provide

from amdb.domain.validators.email import ValidateEmail
from amdb.domain.validators.telegram import ValidateTelegram


class DomainValidatorsProvider(Provider):
    scope = Scope.APP

    email = provide(ValidateEmail, provides=ValidateEmail)
    telegram = provide(ValidateTelegram, provides=ValidateTelegram)
