import json

from redis import Redis

from amdb.domain.entities.user import UserId
from amdb.application.common.constants.export import ExportFormat
from amdb.application.common.constants.sending import SendingMethod


class EnqueueExportAndSendingMyRatingsInRedis:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def __call__(
        self,
        *,
        user_id: UserId,
        export_format: ExportFormat,
        sending_method: SendingMethod,
    ) -> None:
        data = {
            "user_id": user_id.hex,
            "export_format": export_format.value,
            "sending_method": sending_method.value,
        }
        self._redis.lpush(
            "export_and_send_my_ratings_tasks",
            json.dumps(data),
        )
