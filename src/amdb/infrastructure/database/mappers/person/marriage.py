from amdb.domain.entities.person.person import PersonId
from amdb.domain.entities.person import marriage as entity
from amdb.domain.value_objects import Date
from amdb.infrastructure.database.models.person import marriage as model


class MarriageMapper:
    def to_model(
        self,
        *,
        entity: entity.Marriage,
    ) -> model.Marriage:
        if entity.start_date is not None:
            start_year = entity.start_date.year
            start_month = entity.start_date.month
            start_day = entity.start_date.day
        else:
            start_year = None
            start_month = None
            start_day = None

        if entity.end_date is not None:
            end_year = entity.end_date.year
            end_month = entity.end_date.month
            end_day = entity.end_date.day
        else:
            end_year = None
            end_month = None
            end_day = None

        children = []
        for child_id in entity.child_ids:
            child = model.MarriageChild(
                child_id=child_id,
                father_id=entity.husband_id,
                mother_id=entity.wife_id,
            )
            children.append(child)

        return model.Marriage(
            id=entity.id,
            husband_id=entity.husband_id,
            wife_id=entity.wife_id,
            children=children,
            status=entity.status.value,
            start_year=start_year,
            start_month=start_month,
            start_day=start_day,
            end_year=end_year,
            end_month=end_month,
            end_day=end_day,
        )

    def to_entity(
        self,
        *,
        model: model.Marriage,
    ) -> entity.Marriage:
        if model.start_year is not None:
            start_date = Date(
                year=model.start_year,
                month=model.start_month,
                day=model.start_day,
            )
        else:
            start_date = None

        if model.end_year is not None:
            end_date = Date(
                year=model.end_year,
                month=model.end_month,
                day=model.end_day,
            )
        else:
            end_date = None

        return entity.Marriage(
            id=entity.MarriageId(model.id),
            husband_id=PersonId(model.husband_id),
            wife_id=PersonId(model.wife_id),
            child_ids=[PersonId(child.child_id) for child in model.children],
            status=entity.MarriageStatus(model.status),
            start_date=start_date,
            end_date=end_date,
        )
