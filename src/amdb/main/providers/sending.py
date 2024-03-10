from dishka import Provider, Scope, provide

from amdb.application.common.sending.email import SendEmail
from amdb.infrastructure.sending.email import SendFakeEmail


class SendingAdaptersProvider(Provider):
    scope = Scope.APP

    email = provide(SendFakeEmail, provides=SendEmail)
