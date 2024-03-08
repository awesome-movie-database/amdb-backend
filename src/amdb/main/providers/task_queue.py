from dishka import Provider, Scope, provide

from amdb.application.common.task_queue.export_and_send_my_ratings import (
    EnqueueExportAndSendingMyRatings,
)
from amdb.infrastructure.task_queue.export_and_send_my_ratings import (
    EnqueueFakeExportAndSendingMyRatings,
)


class TaskQueueAdaptersProvider(Provider):
    scope = Scope.APP

    export_and_send_ratings = provide(
        EnqueueFakeExportAndSendingMyRatings,
        provides=EnqueueExportAndSendingMyRatings,
    )
