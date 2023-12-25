from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from amdb.infrastructure.database.models.base import Model


class Marriage(Model):
    __tablename__ = "marriages"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )
    husband_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="persons.id", ondelete="CASCADE"),
    )
    wife_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="persons.id", ondelete="CASCADE"),
    )
    children: Mapped[list["MarriageChild"]] = relationship(
        cascade="all, delete-orphan",
    )
    status: Mapped[int]
    start_year: Mapped[Optional[int]]
    start_month: Mapped[Optional[int]]
    start_day: Mapped[Optional[int]]
    end_year: Mapped[Optional[int]]
    end_month: Mapped[Optional[int]]
    end_day: Mapped[Optional[int]]


class MarriageChild(Model):
    __tablename__ = "marriage_children"

    marriage_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="marriages.id", ondelete="CASCADE"),
    )
    child_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="persons.id", ondelete="CASCADE"),
    )

    __table_args__ = (PrimaryKeyConstraint(marriage_id, child_id),)
