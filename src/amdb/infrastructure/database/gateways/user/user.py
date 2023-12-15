from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm.session import Session

from amdb.domain.entities.user import user as entity
from amdb.application.common.interfaces.gateways.user.user import UserGateway
from amdb.infrastructure.database.mappers.user.user import UserMapper
from amdb.infrastructure.database.models.user import user as model


class SQLAlchemyUserGateway(UserGateway):
    def __init__(
        self,
        *,
        session: Session,
        mapper: UserMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def with_id(
        self,
        *,
        user_id: entity.UserId,
    ) -> Optional[entity.User]:
        user_model = self._session.get(
            entity=model.User,
            ident=user_id,
        )
        if user_model:
            return self._mapper.to_entity(
                model=user_model,
            )
        return None

    def with_name(
        self,
        *,
        user_name: str,
    ) -> Optional[entity.User]:
        statement = select(model.User).where(model.User.name == user_name)
        user_model = self._session.scalar(
            statement=statement,
        )
        if user_model:
            return self._mapper.to_entity(
                model=user_model,
            )
        return None

    def save(
        self,
        *,
        user: entity.User,
    ) -> None:
        user_model = self._mapper.to_model(
            entity=user,
        )
        self._session.add(
            instance=user_model,
        )
        self._session.flush(objects=(user_model,))

    def update(
        self,
        *,
        user: entity.User,
    ) -> None:
        user_model = self._mapper.to_model(
            entity=user,
        )
        self._session.merge(
            instance=user_model,
        )
