from amdb.domain.entities.person import person as entity
from amdb.domain.constants.common import Sex
from amdb.domain.value_objects import Date, Place
from amdb.infrastructure.database.models.person import person as model


class PersonMapper:
    def to_model(
        self,
        *,
        entity: entity.Person,
    ) -> model.Person:
        if entity.birth_date is not None:
            birth_year = entity.birth_date.year
            birth_month = entity.birth_date.month
            birth_day = entity.birth_date.day
        else:
            birth_year = None
            birth_month = None
            birth_day = None

        if entity.birth_place is not None:
            birth_country = entity.birth_place.country
            birth_state = entity.birth_place.state
            birth_city = entity.birth_place.city
        else:
            birth_country = None
            birth_state = None
            birth_city = None

        if entity.death_date is not None:
            death_year = entity.death_date.year
            death_month = entity.death_date.month
            death_day = entity.death_date.day
        else:
            death_year = None
            death_month = None
            death_day = None

        if entity.death_place is not None:
            death_country = entity.death_place.country
            death_state = entity.death_place.state
            death_city = entity.death_place.city
        else:
            death_country = None
            death_state = None
            death_city = None

        return model.Person(
            id=entity.id,
            name=entity.name,
            sex=entity.sex.value,
            created_at=entity.created_at,
            birth_year=birth_year,
            birth_month=birth_month,
            birth_day=birth_day,
            birth_country=birth_country,
            birth_state=birth_state,
            birth_city=birth_city,
            death_year=death_year,
            death_month=death_month,
            death_day=death_day,
            death_country=death_country,
            death_state=death_state,
            death_city=death_city,
            updated_at=entity.updated_at,
        )

    def to_entity(
        self,
        *,
        model: model.Person,
    ) -> entity.Person:
        if model.birth_year is not None:
            birth_date = Date(
                year=model.birth_year,
                month=model.birth_month,
                day=model.birth_day,
            )
        else:
            birth_date = None

        if model.birth_country is not None:
            birth_place = Place(
                country=model.birth_country,
                state=model.birth_state,
                city=model.birth_city,
            )
        else:
            birth_place = None

        if model.death_year is not None:
            death_date = Date(
                year=model.death_year,
                month=model.death_month,
                day=model.death_day,
            )
        else:
            death_date = None

        if model.death_country is not None:
            death_place = Place(
                country=model.death_country,
                state=model.death_state,
                city=model.death_city,
            )
        else:
            death_place = None

        return entity.Person(
            id=entity.PersonId(model.id),
            name=model.name,
            sex=Sex(model.sex),
            created_at=model.created_at,
            birth_date=birth_date,
            birth_place=birth_place,
            death_date=death_date,
            death_place=death_place,
            updated_at=model.updated_at,
        )
