from dataclasses import dataclass

from amdb.domain.entities.person.marriage import MarriageId


@dataclass(frozen=True, slots=True)
class DeleteMarriageCommand:
    marriage_id: MarriageId
