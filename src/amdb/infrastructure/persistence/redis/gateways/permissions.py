from typing import Optional

from redis.client import Redis

from amdb.domain.entities.user import UserId


class RedisPermissionsGateway:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def with_user_id(self, user_id: UserId) -> Optional[int]:
        permissions = self._redis.get(f"permissions:user_id:{user_id.hex}")
        if permissions:
            return int(permissions)
        return None

    def set(self, user_id: UserId, permissions: int) -> None:
        self._redis.set(
            name=f"permissions:user_id:{user_id.hex}",
            value=permissions,
        )

    def for_new_user(self) -> int:
        return 4

    def for_create_movie(self) -> int:
        return 2

    def for_delete_movie(self) -> int:
        return 2

    def for_rate_movie(self) -> int:
        return 4

    def for_unrate_movie(self) -> int:
        return 4
