from sqlalchemy.orm import Session

from amdb.application.common.interfaces.unit_of_work import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(
        self,
        *,
        session: Session,
    ) -> None:
        self._session = session

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
