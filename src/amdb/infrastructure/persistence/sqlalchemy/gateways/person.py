from sqlalchemy.orm.session import Session

from amdb.domain.entities.person import Person as PersonEntity
from amdb.infrastructure.persistence.sqlalchemy.mappers.person import PersonMapper


class SQLAlchemyPersonGateway:
    def __init__(
        self,
        session: Session,
        mapper: PersonMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def save(self, person: PersonEntity) -> None:
        person_model = self._mapper.to_model(person)
        self._session.add(person_model)
