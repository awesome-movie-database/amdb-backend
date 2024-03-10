from dishka import Provider, Scope, provide

from amdb.application.common.services import (
    ConvertMyRatingsToFile,
    EnsureCanUseSendingMethod,
)


class ApllicationServicesProvider(Provider):
    scope = Scope.APP

    convert_my_ratings_to_file = provide(
        ConvertMyRatingsToFile,
        provides=ConvertMyRatingsToFile,
    )
    ensure_can_use_sending_method = provide(
        EnsureCanUseSendingMethod,
        provides=EnsureCanUseSendingMethod,
    )
