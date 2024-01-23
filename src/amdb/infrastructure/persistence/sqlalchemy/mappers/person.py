from amdb.domain.entities.person import PersonId, Person as PersonEntity
from amdb.infrastructure.persistence.sqlalchemy.models.person import Person as PersonModel


class PersonMapper:
    def to_model(self, person: PersonEntity) -> PersonModel:
        return PersonModel(
            id=person.id,
            name=person.name,
        )

    def to_entity(self, person: PersonModel) -> PersonEntity:
        return PersonEntity(
            id=PersonId(person.id),
            name=person.name,
        )
