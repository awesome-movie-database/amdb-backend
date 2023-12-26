from typing import Optional

from sqlalchemy import select, inspect
from sqlalchemy.orm import Session

from amdb.domain.entities.person.person import PersonId
from amdb.domain.entities.person import marriage as entity
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.infrastructure.database.mappers.person.marriage import MarriageMapper
from amdb.infrastructure.database.models.person import marriage as model


class SQLAlchemyMarriageGateway(MarriageGateway):
    def __init__(
        self,
        *,
        session: Session,
        mapper: MarriageMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def with_id(
        self,
        *,
        marriage_id: entity.MarriageId,
    ) -> Optional[entity.Marriage]:
        marriage_model = self._session.get(
            entity=model.Marriage,
            ident=marriage_id,
        )
        if marriage_model is not None:
            return self._mapper.to_entity(
                model=marriage_model,
            )
        return None

    def list_with_husband_id(
        self,
        *,
        husband_id: PersonId,
    ) -> list[entity.Marriage]:
        statement = select(model.Marriage).filter(model.Marriage.husband_id == husband_id)
        marriage_models = self._session.scalars(
            statement=statement,
        )
        marriage_entities = []
        for marriage_model in marriage_models:
            marriage_entity = self._mapper.to_entity(
                model=marriage_model,
            )
            marriage_entities.append(marriage_entity)

        return marriage_entities

    def list_with_wife_id(
        self,
        *,
        wife_id: PersonId,
    ) -> list[entity.Marriage]:
        statement = select(model.Marriage).filter(model.Marriage.wife_id == wife_id)
        marriage_models = self._session.scalars(
            statement=statement,
        )
        marriage_entities = []
        for marriage_model in marriage_models:
            marriage_entity = self._mapper.to_entity(
                model=marriage_model,
            )
            marriage_entities.append(marriage_entity)

        return marriage_entities

    def save(
        self,
        *,
        marriage: entity.Marriage,
    ) -> None:
        marriage_model = self._mapper.to_model(
            entity=marriage,
        )
        self._session.add(
            instance=marriage_model,
        )
        self._session.flush(
            objects=(marriage_model,),
        )

    def update(
        self,
        *,
        marriage: entity.Marriage,
    ) -> None:
        marriage_model = self._mapper.to_model(
            entity=marriage,
        )
        self._session.merge(
            instance=marriage_model,
        )

    def delete(
        self,
        *,
        marriage: entity.Marriage,
    ) -> None:
        marriage_model = self._mapper.to_model(
            entity=marriage,
        )
        marriage_model_insp = inspect(
            subject=marriage_model,
        )
        if marriage_model_insp.persistent:
            self._session.delete(
                instance=marriage_model,
            )
        elif marriage_model_insp.pending:
            self._session.expunge(
                instance=marriage_model,
            )
