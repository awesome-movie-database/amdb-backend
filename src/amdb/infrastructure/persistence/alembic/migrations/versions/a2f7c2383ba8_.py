"""
Add permissions table,
Fill permission table with default data,
Make type column string in reviews table,
Add email column in users table

Revision ID: a2f7c2383ba8
Revises: 65f8840f4494
Create Date: 2024-02-24 00:59:16.630215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a2f7c2383ba8"
down_revision: Union[str, None] = "65f8840f4494"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "permissions",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False, default=30),
        sa.PrimaryKeyConstraint("user_id"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
    )
    op.execute(
        """
        INSERT INTO permissions (user_id)
        (SELECT u.id FROM users u)
        """,
    )
    with op.batch_alter_table("reviews") as batch_op:
        batch_op.alter_column(
            "type",
            new_column_name="old_type",
        )
        batch_op.add_column(
            sa.Column("type", sa.String(), nullable=True),
        )
    op.execute(
        """
        UPDATE reviews
        SET type =
        (
            SELECT
                CASE
                    WHEN r.old_type = 0 THEN 'neutral'
                    WHEN r.old_type = 1 THEN 'positive'
                    WHEN r.old_type = 2 THEN 'negative'
                END
            FROM reviews r
        )
        """,
    )
    with op.batch_alter_table("reviews") as batch_op:
        batch_op.drop_column("old_type")
        batch_op.alter_column(
            "type",
            nullable=False,
        )
    op.add_column(
        "users",
        sa.Column("email", sa.String(), nullable=True, unique=True),
    )


def downgrade() -> None:
    op.drop_table("permissions")
    with op.batch_alter_table("reviews") as batch_op:
        batch_op.alter_column(
            "type",
            new_column_name="old_type",
        )
        batch_op.add_column(
            sa.Column("type", sa.Integer(), nullable=True),
        )
    op.execute(
        """
        UPDATE reviews
        SET type =
        (
            SELECT
                CASE
                    WHEN r.old_type = 'neutral' THEN 0
                    WHEN r.old_type = 'positive' THEN 1
                    WHEN r.old_type = 'negative' THEN 2
                END
            FROM reviews r
        )
        """,
    )
    with op.batch_alter_table("reviews") as batch_op:
        batch_op.drop_column("old_type")
        batch_op.alter_column(
            "type",
            nullable=False,
        )
    op.drop_column("users", "email")
