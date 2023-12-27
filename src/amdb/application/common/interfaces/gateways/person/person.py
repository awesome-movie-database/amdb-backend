from typing import Optional, Protocol

from amdb.domain.entities.person.person import PersonId, Person


class PersonGateway(Protocol):
    def with_id(
        self,
        *,
        person_id: PersonId,
    ) -> Optional[Person]:
        raise NotImplementedError

    def list_with_ids(
        self,
        *person_ids: PersonId,
    ) -> tuple[list[Person], list[PersonId]]:
        """
        Returns tuple of persons and person ids that
        were not found
        """
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

    def update_list(
        self,
        *,
        persons: list[Person],
    ) -> None:
        raise NotImplementedError
