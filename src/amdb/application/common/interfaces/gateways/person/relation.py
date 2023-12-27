from typing import Optional, Protocol

from amdb.domain.entities.person.person import PersonId
from amdb.domain.entities.person.relation import Relation


class RelationGateway(Protocol):
    def with_person_id_and_relative_id(
        self,
        *,
        person_id: PersonId,
        relative_id: PersonId,
    ) -> Optional[Relation]:
        raise NotImplementedError

    def save(
        self,
        *,
        relation: Relation,
    ) -> None:
        raise NotImplementedError
