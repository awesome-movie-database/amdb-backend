from datetime import timedelta
from typing import Optional, cast

from redis import Redis

from amdb.domain.entities.user import UserId


CACHE_TIME = timedelta(hours=24)


class PermissionsMapperCacheProvider:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def with_user_id(self, user_id: UserId) -> Optional[int]:
        permissions = self._redis.get(f"permissions:user_id:{user_id.hex}")
        if permissions:
            return int(cast(str, permissions))
        return None

    def set(self, user_id: UserId, permissions: int) -> None:
        self._redis.set(
            name=f"permissions:user_id:{user_id.hex}",
            value=permissions,
            ex=CACHE_TIME,
        )
