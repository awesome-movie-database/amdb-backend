"""
Test can find forgotten downgrade methods, undeleted data types in downgrade
methods, typos and many other errors.

Does not require any maintenance - you just add it once to check 80% of typos
and mistakes in migrations forever.

https://github.com/alvassin/alembic-quickstart
"""
import alembic.config
import alembic.command
import alembic.script


def get_revisions(alembic_config: alembic.config.Config) -> list[alembic.script.Script]:
    # Get directory object with Alembic migrations
    revisions_dir = alembic.script.ScriptDirectory.from_config(alembic_config)

    # Get & sort migrations, from first to last
    revisions: list[alembic.script.Script] = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()

    return revisions


def test_migrations_stairway(alembic_config: alembic.config.Config):
    for revision in get_revisions(alembic_config):
        alembic.command.upgrade(alembic_config, revision.revision)

        # We need -1 for downgrading first migration (its down_revision is None)
        alembic.command.downgrade(alembic_config, revision.down_revision or "-1")  # type: ignore
        alembic.command.upgrade(alembic_config, revision.revision)
