from typing import Optional

from sqlalchemy.orm import Session

from amdb.domain.entities.user.user import UserId
from amdb.domain.entities.user import profile as entity
from amdb.application.common.interfaces.gateways.user.profile import ProfileGateway
from amdb.infrastructure.database.mappers.user.profile import ProfileMapper
from amdb.infrastructure.database.models.user import profile as model


class SQLAlchemyProfileGateway(ProfileGateway):
    def __init__(
        self,
        *,
        session: Session,
        mapper: ProfileMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def with_user_id(
        self,
        *,
        user_id: UserId,
    ) -> Optional[entity.Profile]:
        profile_model = self._session.get(
            entity=model.Profile,
            ident=user_id,
        )
        if profile_model:
            return self._mapper.to_entity(
                model=profile_model,
            )
        return None

    def save(
        self,
        *,
        profile: entity.Profile,
    ) -> None:
        profile_model = self._mapper.to_model(
            entity=profile,
        )
        self._session.add(
            instance=profile_model,
        )
        self._session.flush(
            objects=(profile_model,),
        )

    def update(
        self,
        *,
        profile: entity.Profile,
    ) -> None:
        profile_model = self._mapper.to_model(
            entity=profile,
        )
        self._session.merge(
            instance=profile_model,
        )
