from dishka import Provider, Scope, provide

from amdb.domain.validators.email import ValidateEmail


class DomainValidatorsProvider(Provider):
    scope = Scope.APP

    email = provide(ValidateEmail, provides=ValidateEmail)
