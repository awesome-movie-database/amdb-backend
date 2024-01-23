from typing import Protocol

from amdb.domain.entities.person import Person


class PersonGateway(Protocol):
    def save(self, person: Person) -> None:
        raise NotImplementedError
