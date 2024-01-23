"""Add person table

Revision ID: 9bd5fe6d17c4
Revises: 9e92de201574
Create Date: 2024-01-23 15:55:52.698254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9bd5fe6d17c4"
down_revision: Union[str, None] = "9e92de201574"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "persons",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("persons")
