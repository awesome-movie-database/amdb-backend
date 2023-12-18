from uuid import UUID

from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from amdb.infrastructure.database.models.base import Model


class Relation(Model):
    __tablename__ = "relations"

    person_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="persons.id", ondelete="CASCADE"),
    )
    relative_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="persons.id", ondelete="CASCADE"),
    )
    type: Mapped[int]

    __table_args__ = (PrimaryKeyConstraint(person_id, relative_id),)
