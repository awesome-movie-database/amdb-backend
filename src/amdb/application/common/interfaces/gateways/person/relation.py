from typing import Protocol

from amdb.domain.entities.person.relation import Relation


class RelationGateway(Protocol):
    def save(
        self,
        *,
        relation: Relation,
    ) -> None:
        raise NotImplementedError
