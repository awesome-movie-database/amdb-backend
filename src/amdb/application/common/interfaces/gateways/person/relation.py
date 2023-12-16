from typing import Protocol

from amdb.domain.entities.person.relation import Relation


class RelationGateway(Protocol):
    def save_list(
        self,
        *,
        relations: list[Relation],
    ) -> None:
        raise NotImplementedError
