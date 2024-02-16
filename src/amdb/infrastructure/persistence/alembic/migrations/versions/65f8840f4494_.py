"""
Add uuid7 function,
Add id column to ratings table,
Add primary key constraint on id in ratings table,
Add unique constraint on pair of user_id and movie_id in ratings table,
Add unique constraint on pair of user_id and movie_id in reviews table

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
    op.execute(
        """
        /*
        * MIT License
        *
        * Copyright (c) 2023 Fabio Lima
        *
        *  Permission is hereby granted, free of charge, to any person obtaining a copy
        *  of this software and associated documentation files (the "Software"), to deal
        *  in the Software without restriction, including without limitation the rights
        *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        *  copies of the Software, and to permit persons to whom the Software is
        *  furnished to do so, subject to the following conditions:
        *
        *  The above copyright notice and this permission notice shall be included in
        *  all copies or substantial portions of the Software.
        *
        *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        *  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        *  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        *  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        *  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
        *  THE SOFTWARE.
        */

        /**
        * Returns a time-ordered with Unix Epoch UUID (UUIDv7).
        *
        * Referencies:
        * - https://github.com/uuid6/uuid6-ietf-draft
        * - https://github.com/ietf-wg-uuidrev/rfc4122bis
        *
        * MIT License.
        *
        * Tags: uuid guid uuid-generator guid-generator generator time order rfc4122 rfc-4122
        */
        create or replace function uuid7() returns uuid as $$
        declare
            v_time timestamp with time zone:= null;
            v_secs bigint := null;
            v_usec bigint := null;

            v_timestamp bigint := null;
            v_timestamp_hex varchar := null;

            v_random bigint := null;
            v_random_hex varchar := null;

            v_bytes bytea;

            c_variant bit(64):= x'8000000000000000'; -- RFC-4122 variant: b'10xx...'
        begin

            -- Get seconds and micros
            v_time := clock_timestamp();
            v_secs := EXTRACT(EPOCH FROM v_time);
            v_usec := mod(EXTRACT(MICROSECONDS FROM v_time)::numeric, 10^6::numeric);

            -- Generate timestamp hexadecimal (and set version 7)
            v_timestamp := (((v_secs * 1000) + div(v_usec, 1000))::bigint << 12) | (mod(v_usec, 1000) << 2);
            v_timestamp_hex := lpad(to_hex(v_timestamp), 16, '0');
            v_timestamp_hex := substr(v_timestamp_hex, 2, 12) || '7' || substr(v_timestamp_hex, 14, 3);

            -- Generate the random hexadecimal (and set variant b'10xx')
            v_random := ((random()::numeric * 2^62::numeric)::bigint::bit(64) | c_variant)::bigint;
            v_random_hex := lpad(to_hex(v_random), 16, '0');

            -- Concat timestemp and random hexadecimal
            v_bytes := decode(v_timestamp_hex || v_random_hex, 'hex');

            return encode(v_bytes, 'hex')::uuid;

        end $$ language plpgsql;
        """,
    )
    with op.batch_alter_table("ratings") as batch_op:
        batch_op.add_column(
            sa.Column("id", sa.Uuid(), nullable=False, default="uuid7()")
        )
        batch_op.drop_constraint("pk_ratings", type_="primary")
        batch_op.create_primary_key("pk_ratings", ["id"])
        batch_op.create_unique_constraint(
            "uq_ratings", ("user_id", "movie_id")
        )
    op.create_unique_constraint(
        "uq_reviews", "reviews", ("user_id", "movie_id")
    )


def downgrade() -> None:
    with op.batch_alter_table("ratings") as batch_op:
        batch_op.drop_constraint("pk_ratings", type_="primary")
        batch_op.drop_column("id")
        batch_op.create_primary_key("pk_ratings", ["user_id", "movie_id"])
        batch_op.drop_constraint("uq_ratings")
    op.drop_constraint("uq_reviews", "reviews")
    op.execute("DROP FUNCTION uuid7")
