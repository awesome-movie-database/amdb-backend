from typing import Optional, Protocol

from amdb.domain.entities.person.person import PersonId, Person


class PersonGateway(Protocol):
    def with_id(
        self,
        *,
        person_id: PersonId,
    ) -> Optional[Person]:
        raise NotImplementedError

    def save(
        self,
        *,
        person: Person,
    ) -> None:
        raise NotImplementedError

    def update(
        self,
        *,
        person: Person,
    ) -> None:
        raise NotImplementedError
