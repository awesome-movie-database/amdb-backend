from typing import Protocol

from amdb.domain.entities.person.marriage import Marriage


class MarriageGateway(Protocol):
    def save_list(
        self,
        *,
        marriages: list[Marriage],
    ) -> None:
        raise NotImplementedError
