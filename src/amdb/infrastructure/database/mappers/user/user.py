from amdb.domain.entities.user import user as entity
from amdb.domain.constants.common import Sex
from amdb.domain.value_objects import Place
from amdb.infrastructure.database.models.user import user as model


class UserMapper:
    def to_model(
        self,
        *,
        entity: entity.User,
    ) -> model.User:
        if entity.location is not None:
            country = entity.location.country
            state = entity.location.state
            city = entity.location.city
        else:
            country = None
            state = None
            city = None

        return model.User(
            id=entity.id,
            name=entity.name,
            password=entity.password,
            is_active=entity.is_active,
            is_verified=entity.is_verified,
            created_at=entity.created_at,
            email=entity.email,
            birth_date=entity.birth_date,
            country=country,
            state=state,
            city=city,
            verified_at=entity.verified_at,
            updated_at=entity.updated_at,
        )

    def to_entity(
        self,
        *,
        model: model.User,
    ) -> entity.User:
        if model.country is not None:
            location = Place(
                country=model.country,
                state=model.state,
                city=model.city,
            )
        else:
            location = None

        if model.sex is not None:
            sex = Sex(model.sex)
        else:
            sex = None

        return entity.User(
            id=entity.UserId(model.id),
            name=model.name,
            password=model.password,
            is_active=model.is_active,
            is_verified=model.is_verified,
            created_at=model.created_at,
            email=model.email,
            sex=sex,
            birth_date=model.birth_date,
            location=location,
            verified_at=model.verified_at,
            updated_at=model.verified_at,
        )
