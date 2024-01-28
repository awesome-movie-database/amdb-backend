"""
Add id column to ratings table,
Add primary key constraint on id in ratings table,
Add unique constraint on pair of user_id and movie_id in ratings table

Revision ID: 65f8840f4494
Revises: 85a348467b90
Create Date: 2024-01-27 23:16:38.514162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "65f8840f4494"
down_revision: Union[str, None] = "85a348467b90"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("ratings") as batch_op:
        batch_op.add_column(sa.Column("id", sa.Uuid(), nullable=False))
        batch_op.drop_constraint("pk_ratings", type_="primary")
        batch_op.create_primary_key("pk_ratings", ["id"])
        batch_op.create_unique_constraint("uq_ratings", ("user_id", "movie_id"))


def downgrade() -> None:
    with op.batch_alter_table("ratings") as batch_op:
        batch_op.drop_constraint("pk_ratings", type_="primary")
        batch_op.drop_column("id")
        batch_op.create_primary_key("pk_ratings", ["user_id", "movie_id"])
        batch_op.drop_constraint("uq_ratings")
