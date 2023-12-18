from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from amdb.infrastructure.database.models.base import Model


class Marriage(Model):
    __tablename__ = "marriages"

    husband_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="persons.id", ondelete="CASCADE"),
    )
    wife_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="persons.id", ondelete="CASCADE"),
    )
    children: Mapped[list["MarriageChild"]] = relationship()
    status: Mapped[int]
    start_year: Mapped[Optional[int]]
    start_month: Mapped[Optional[int]]
    start_day: Mapped[Optional[int]]
    end_year: Mapped[Optional[int]]
    end_month: Mapped[Optional[int]]
    end_day: Mapped[Optional[int]]


class MarriageChild(Model):
    __tablename__ = "marriage_children"

    child_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="persons.id", ondelete="CASCADE"),
    )
    father_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="persons.id", ondelete="CASCADE"),
    )
    mother_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="persons.id", ondelete="CASCADE"),
    )

    __table_args__ = (PrimaryKeyConstraint(child_id, father_id, mother_id),)
