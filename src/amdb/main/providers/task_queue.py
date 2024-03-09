from dishka import Provider, Scope, provide

from amdb.application.common.task_queue.export_and_send_my_ratings import (
    EnqueueExportAndSendingMyRatings,
)
from amdb.infrastructure.persistence.redis.task_queue.export_and_send_my_ratings import (
    EnqueueExportAndSendingMyRatingsInRedis,
)


class TaskQueueAdaptersProvider(Provider):
    scope = Scope.APP

    export_and_send_ratings = provide(
        EnqueueExportAndSendingMyRatingsInRedis,
        provides=EnqueueExportAndSendingMyRatings,
    )
