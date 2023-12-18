from sqlalchemy.orm import Session

from amdb.domain.entities.person import marriage as entity
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.infrastructure.database.mappers.person.marriage import MarriageMapper


class SQLAlchemyMarriageGateway(MarriageGateway):
    def __init__(
        self,
        *,
        session: Session,
        mapper: MarriageMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def save_list(
        self,
        *,
        marriages: list[entity.Marriage],
    ) -> None:
        marriage_models = []
        for marriage_entity in marriages:
            marriage_model = self._mapper.to_model(
                entity=marriage_entity,
            )
            marriage_models.append(marriage_model)
            self._session.add(
                instance=marriage_model,
            )
        self._session.flush(
            objects=marriage_models,
        )
