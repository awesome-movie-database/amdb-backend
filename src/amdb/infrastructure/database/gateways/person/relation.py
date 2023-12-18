from typing import Optional

from sqlalchemy.orm import Session

from amdb.domain.entities.person.person import PersonId
from amdb.domain.entities.person import relation as entity
from amdb.application.common.interfaces.gateways.person.relation import RelationGateway
from amdb.infrastructure.database.mappers.person.relation import RelationMapper
from amdb.infrastructure.database.models.person import relation as model


class SQLAlchemyRelationGateway(RelationGateway):
    def __init__(
        self,
        *,
        session: Session,
        mapper: RelationMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def with_person_id_and_relative_id(
        self,
        person_id: PersonId,
        relative_id: PersonId,
    ) -> Optional[entity.Relation]:
        relation_model = self._session.get(
            entity=model.Relation,
            ident={"person_id": person_id, "relative_id": relative_id},
        )
        if relation_model is not None:
            return self._mapper.to_entity(
                model=relation_model,
            )
        return None

    def save_list(
        self,
        *,
        relations: list[entity.Relation],
    ) -> None:
        relation_models = []
        for relation_entity in relations:
            relation_model = self._mapper.to_model(
                entity=relation_entity,
            )
            relation_models.append(relation_model)
            self._session.add(
                instance=relation_model,
            )
        self._session.flush(
            objects=relation_models,
        )
