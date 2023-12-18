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

    def save(
        self,
        *,
        relation: entity.Relation,
    ) -> None:
        relation_model = self._mapper.to_model(
            entity=relation,
        )
        self._session.add(
            instance=relation_model,
        )
        self._session.flush(
            objects=(relation_model,),
        )
