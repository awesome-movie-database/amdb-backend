"""Add release_date column to movies table

Revision ID: 85a348467b90
Revises: 9e92de201574
Create Date: 2024-01-25 18:16:41.464281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "85a348467b90"
down_revision: Union[str, None] = "9e92de201574"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("movies", sa.Column("release_date", sa.String))


def downgrade() -> None:
    op.drop_column("movies", "release_date")
