from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from amdb.domain.entities.person import person as entity
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.infrastructure.database.mappers.person.person import PersonMapper
from amdb.infrastructure.database.models.person import person as model


class SQLAlchemyPersonGateway(PersonGateway):
    def __init__(
        self,
        *,
        session: Session,
        mapper: PersonMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def with_id(
        self,
        *,
        person_id: entity.PersonId,
    ) -> Optional[entity.Person]:
        person_model = self._session.get(
            entity=model.Person,
            ident=person_id,
        )
        if person_model:
            return self._mapper.to_entity(
                model=person_model,
            )
        return None

    def list_with_ids(
        self,
        *person_ids: entity.PersonId,
    ) -> tuple[list[entity.Person], list[entity.PersonId]]:
        statement = select(model.Person).filter(model.Person.id.in_(person_ids))
        person_models = self._session.scalars(
            statement=statement,
        )
        person_entities = [
            self._mapper.to_entity(model=person_model) for person_model in person_models
        ]

        missing_person_ids = []
        if len(person_entities) != len(person_ids):
            fetched_person_ids = [person_entity.id for person_entity in person_entities]

            for person_id in person_ids:
                if person_id in fetched_person_ids:
                    continue
                missing_person_ids.append(person_id)

        return person_entities, missing_person_ids

    def save(
        self,
        *,
        person: entity.Person,
    ) -> None:
        person_model = self._mapper.to_model(
            entity=person,
        )
        self._session.add(
            instance=person_model,
        )
        self._session.flush(
            objects=(person_model,),
        )

    def update(
        self,
        *persons: entity.Person,
    ) -> None:
        for person in persons:
            person_model = self._mapper.to_model(
                entity=person,
            )
            self._session.merge(
                instance=person_model,
            )
