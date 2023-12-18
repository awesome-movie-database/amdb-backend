from amdb.domain.entities.person.person import PersonId
from amdb.domain.entities.person import relation as entity
from amdb.infrastructure.database.models.person import relation as model


class RelationMapper:
    def to_model(
        self,
        *,
        entity: entity.Relation,
    ) -> model.Relation:
        return model.Relation(
            person_id=entity.person_id,
            relative_id=entity.relative_id,
            type=entity.type.value,
        )

    def to_entity(
        self,
        *,
        model: model.Relation,
    ) -> entity.Relation:
        return entity.Relation(
            person_id=PersonId(model.person_id),
            relative_id=PersonId(model.relative_id),
            type=entity.RelativeType(model.type),
        )
