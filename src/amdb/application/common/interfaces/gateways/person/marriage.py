from typing import Protocol

from amdb.domain.entities.person.person import PersonId
from amdb.domain.entities.person.marriage import Marriage


class MarriageGateway(Protocol):
    def list_with_husband_id(
        self,
        *,
        husband_id: PersonId,
    ) -> list[Marriage]:
        raise NotImplementedError

    def list_with_wife_id(
        self,
        *,
        wife_id: PersonId,
    ) -> list[Marriage]:
        raise NotImplementedError

    def save(
        self,
        *,
        marriage: Marriage,
    ) -> None:
        raise NotImplementedError
