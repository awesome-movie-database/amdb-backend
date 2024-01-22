import pytest
import alembic.config
import psycopg2

from amdb.infrastructure.persistence.alembic.config import ALEMBIC_CONFIG


@pytest.fixture(scope="package")
def alembic_config(postgres_url: str) -> alembic.config.Config:
    alembic_cfg = alembic.config.Config(ALEMBIC_CONFIG)
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)
    return alembic_cfg


@pytest.fixture(scope="package", autouse=True)
def clear_database(postgres_url: str) -> None:
    connection = psycopg2.connect(postgres_url)
    cursor = connection.cursor()

    yield

    cursor.execute(
        """
        DO $$
        DECLARE tablenames text;
        BEGIN
            tablenames := string_agg('"' || tablename || '"', ', ')
                FROM pg_tables WHERE schemaname = 'public';
            EXECUTE 'DROP TABLE ' || tablenames;
        END; $$
        """,
    )
    connection.commit()

    cursor.close()
    connection.close()
