from amdb.domain.entities.person import PersonId, Person


class CreatePerson:
    def __call__(
        self,
        *,
        id: PersonId,
        name: str,
    ) -> Person:
        return Person(
            id=id,
            name=name,
        )
