from typing import Optional

from amdb.domain.entities.user import UserId
from amdb.infrastructure.persistence.sqlalchemy.mappers.permissions import (
    PermissionsMapper,
)
from amdb.infrastructure.persistence.redis.cache.permissions_mapper import (
    PermissionsMapperCacheProvider,
)


class CachingPermissionsMapper:
    def __init__(
        self,
        *,
        permissions_mapper: PermissionsMapper,
        cache_provider: PermissionsMapperCacheProvider,
    ) -> None:
        self._permissions_mapper = permissions_mapper
        self._cache_provider = cache_provider

    def with_user_id(self, user_id: UserId) -> Optional[int]:
        permissions_from_cache = self._cache_provider.with_user_id(user_id)
        if permissions_from_cache:
            return permissions_from_cache

        permissions_from_database = self._permissions_mapper.with_user_id(
            user_id,
        )
        if permissions_from_database:
            self._cache_provider.set(
                user_id=user_id,
                permissions=permissions_from_database,
            )

        return permissions_from_database

    def set(self, user_id: UserId, permissions: int) -> None:
        self._permissions_mapper.set(
            user_id=user_id,
            permissions=permissions,
        )
        self._cache_provider.set(
            user_id=user_id,
            permissions=permissions,
        )

    def for_new_user(self) -> int:
        return (
            self.for_login()
            + self.for_rate_movie()
            + self.for_unrate_movie()
            + self.for_review_movie()
        )

    def for_login(self) -> int:
        return 2

    def for_rate_movie(self) -> int:
        return 4

    def for_unrate_movie(self) -> int:
        return 8

    def for_review_movie(self) -> int:
        return 16
