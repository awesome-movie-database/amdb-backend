from sqlalchemy.orm import Session

from amdb.domain.entities.person import relation as entity
from amdb.application.common.interfaces.gateways.person.relation import RelationGateway
from amdb.infrastructure.database.mappers.person.relation import RelationMapper


class SQLAlchemyRelationGateway(RelationGateway):
    def __init__(
        self,
        *,
        session: Session,
        mapper: RelationMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

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
