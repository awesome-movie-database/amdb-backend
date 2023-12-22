from sqlalchemy.orm import Session

# from amdb.infrastructure.database.mappers import user as user_mappers
# from amdb.infrastructure.database.mappers import person as person_mappers
# from amdb.infrastructure.database.gateways import user as user_gateways
# from amdb.infrastructure.database.gateways import person as person_gateways
from amdb.infrastructure.database.gateways.user.user import SQLAlchemyUserGateway
from amdb.infrastructure.database.gateways.user.profile import SQLAlchemyProfileGateway
from amdb.infrastructure.database.gateways.person.person import SQLAlchemyPersonGateway
from amdb.infrastructure.database.gateways.person.marriage import SQLAlchemyMarriageGateway
from amdb.infrastructure.database.gateways.person.relation import SQLAlchemyRelationGateway
from amdb.infrastructure.database.mappers.user.user import UserMapper
from amdb.infrastructure.database.mappers.user.profile import ProfileMapper
from amdb.infrastructure.database.mappers.person.person import PersonMapper
from amdb.infrastructure.database.mappers.person.marriage import MarriageMapper
from amdb.infrastructure.database.mappers.person.relation import RelationMapper
from .unit_of_work import SQLAlchemyUnitOfWork


class GatewayFactory:
    def __init__(
        self,
        *,
        session: Session,
    ) -> None:
        self._session = session

    def create_user_gateway(self) -> SQLAlchemyUserGateway:
        return SQLAlchemyUserGateway(
            session=self._session,
            mapper=UserMapper(),
        )

    def create_profile_gateway(self) -> SQLAlchemyProfileGateway:
        return SQLAlchemyProfileGateway(
            session=self._session,
            mapper=ProfileMapper(),
        )

    def create_person_gateway(self) -> SQLAlchemyPersonGateway:
        return SQLAlchemyPersonGateway(
            session=self._session,
            mapper=PersonMapper(),
        )

    def create_marriage_gateway(self) -> SQLAlchemyMarriageGateway:
        return SQLAlchemyMarriageGateway(
            session=self._session,
            mapper=MarriageMapper(),
        )

    def create_relation_gateway(self) -> SQLAlchemyRelationGateway:
        return SQLAlchemyRelationGateway(
            session=self._session,
            mapper=RelationMapper(),
        )

    def create_unit_of_wok(self) -> SQLAlchemyUnitOfWork:
        return SQLAlchemyUnitOfWork(
            session=self._session,
        )
